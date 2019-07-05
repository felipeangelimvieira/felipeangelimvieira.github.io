import React from "react";
import Landing from "../components/landing";
import About from '../components/about';

import styles from '../styles/global.css';


export default () => (<div className={styles.body}>
        <Landing />
        <About />
</div>)
