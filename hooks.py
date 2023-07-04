import asyncio
import platform
from glob import iglob
from os import makedirs, path, remove, removedirs
from pprint import pformat
from time import time
from traitlets.config import Config
import nbformat
from mkdocs.config import base, config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from mkdocs.utils import log
from nbconvert import MarkdownExporter

from nbconvert.preprocessors import (
    CellExecutionError,
    ExecutePreprocessor,
    TagRemovePreprocessor,
)  # pyright: ignore[reportPrivateImportUsage]

_src_files = []


def on_config(config, **kwargs):
    config["input_dir"] = "docs/blogsource/"
    config["output_dir"] = "blog/"
    config["recursive"] = True
    config["execute_enabled"] = False
    config["execute_options"] = {
        "run_path": None,
        "kernel_name": None,
        "timeout": None,
        "write_back": False,
        "exit_on_error": True,
    }
    return config


def on_files(files, config, **kwargs):
    log.debug("[Custom NbConvertPlugin] config: %s", pformat(config))
    # deal with dirs
    config_file_dir = path.dirname(config["config_file_path"])
    input_dir = path.normpath(config["input_dir"])
    output_dir = path.realpath(
        path.join(config["docs_dir"], path.normpath(config["output_dir"]))
    )
    if not path.isabs(input_dir):
        input_dir = path.realpath(path.join(config_file_dir, input_dir))
    # glob match
    nb_finder = iglob(
        path.join(config_file_dir, input_dir, "**", "*.ipynb"),
        recursive=config["recursive"],
    )

    c = Config()

    # Configure tag removal - be sure to tag your cells to remove  using the
    # words remove_cell to remove cells. You can also modify the code to use
    # a different tag word
    c.TagRemovePreprocessor.remove_cell_tags = ("remove_cell",)
    c.TagRemovePreprocessor.remove_all_outputs_tags = ("remove_output",)
    c.TagRemovePreprocessor.remove_input_tags = ("remove_input",)
    c.TagRemovePreprocessor.enabled = True

    # Exporter
    exporter = MarkdownExporter(config=c)
    exporter.register_preprocessor(TagRemovePreprocessor(config=c), True)
    # Pre-execute args
    exe_opts = exe_path = exe_save = exe_exit_on_error = None
    if config.get("execute_enabled"):
        _opts = config.get("execute_options") or {}
        exe_opts = {
            k: v
            for k, v in _opts.items()
            if k in ("timeout", "kernel_name") and v is not None
        }
        exe_path, exe_save, exe_exit_on_error = (
            _opts.get(a) for a in ("run_path", "write_back", "exit_on_error")
        )
        # On windows:
        #   Proactor event loop does not implement add_reader family of methods required for zmq.
        #   Registering an additional selector thread for add_reader support via tornado.
        #   Use `asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())` to avoid this warning.
        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # Converting
    for i, nb_path in enumerate(nb_finder, 1):
        # Prepare output file/dir
        nb_dirname, nb_basename = path.split(nb_path)
        nb_basename_root, _ = path.splitext(nb_basename)
        nb_subdir = path.relpath(nb_dirname, input_dir)
        md_dir = path.join(output_dir, nb_subdir)
        md_basename = f"{nb_basename_root}.md"
        md_path = path.join(md_dir, md_basename)
        md_rel_dir = path.relpath(md_dir, config["docs_dir"])
        md_rel_path = path.join(md_rel_dir, md_basename)
        file_obj = File(
            path=md_rel_path,
            src_dir=config["docs_dir"],
            dest_dir=config["site_dir"],
            use_directory_urls=config["use_directory_urls"],
        )
        #
        log.info("[Custom NbConvertPlugin] (%d) %r => %r", i, nb_path, file_obj)
        # read out
        with open(nb_path, encoding="utf-8") as fp:
            nb = nbformat.read(fp, nbformat.NO_CONVERT)
        # pre-execute
        if exe_opts is not None:
            log.debug("[Custom NbConvertPlugin] (%d) notebook execution start", i)
            ts = time()
            exe_completed = False
            ep = ExecutePreprocessor(**exe_opts)
            try:
                ep.preprocess(
                    nb, {"metadata": {"path": exe_path if exe_path else input_dir}}
                )
            except CellExecutionError as err:
                if exe_exit_on_error:
                    raise
                exe_completed = True
                log.error(
                    "[Custom NbConvertPlugin] (%d) notebook execution error(%.3fs): %s",
                    i,
                    time() - ts,
                    err,
                )
            else:
                exe_completed = True
                log.debug(
                    "[Custom NbConvertPlugin] (%d) notebook execution finish(%.3fs)",
                    i,
                    time() - ts,
                )
            finally:
                if exe_save and exe_completed:
                    log.debug("[Custom NbConvertPlugin] (%d) save notebook", i)
                    with open(nb_path, "w", encoding="utf-8") as fp:
                        nbformat.write(nb, fp)
        # convert
        body, resources = exporter.from_notebook_node(nb)
        # save exported
        makedirs(md_dir, exist_ok=True)
        with open(md_path, "w", encoding="utf-8") as fp:
            fp.write(body)
        for resource_name, resource_data in resources["outputs"].items():
            resource_src_dir = path.dirname(file_obj.abs_src_path)
            resource_src_path = path.join(resource_src_dir, resource_name)
            makedirs(resource_src_dir, exist_ok=True)
            with open(resource_src_path, "wb") as fp:
                fp.write(resource_data)
            _src_files.append(resource_src_path)
            resource_dest_dir = path.dirname(file_obj.abs_dest_path)
            resource_dest_path = path.join(resource_dest_dir, resource_name)
            log.debug(
                "[Custom NbConvertPlugin] (%d) resource output(%dBytes): %s => %s",
                i,
                len(resource_data),
                resource_name,
                resource_dest_path,
            )
            makedirs(resource_dest_dir, exist_ok=True)
            with open(resource_dest_path, "wb") as fp:
                fp.write(resource_data)

        _src_files.append(file_obj.abs_src_path)
        files.append(file_obj)
    return files


def on_post_build(config, **kwargs):
    for file in _src_files:
        log.debug("[Custom NbConvertPlugin] remove: %r", file)
        remove(file)
    output_dir = path.join(config["docs_dir"], path.normpath(config["output_dir"]))
    log.debug("[Custom NbConvertPlugin] removedirs: %r", output_dir)
    try:
        removedirs(output_dir)
    except OSError as err:
        log.warning(
            "[Custom NbConvertPlugin] OSError on removedirs %r: %s", output_dir, err
        )
