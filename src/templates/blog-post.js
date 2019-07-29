// Borrowed from gatsby-starter-blog

import React from "react"
import { Link, graphql } from "gatsby"
import { rhythm, scale } from "../utils/typography"

import styles from '../styles/blog-post.module.css'
import 'katex/dist/katex.min.css'
import Header from '../components/Header'

class BlogPostTemplate extends React.Component {
  render() {
    
    const post = this.props.data.markdownRemark
    const siteTitle = this.props.data.site.siteMetadata.title
    const { previous, next } = this.props.pageContext

    return (
        <div className = {styles.body}>
          <Header />
        <div className={styles.container}>
        
        <h1
          className={styles.title}
        >
          {post.frontmatter.title}
        </h1>
        <p
          className = {styles.date}
        >
          {post.frontmatter.date}
        </p>
        <div style={{textAlign: "justify"}} dangerouslySetInnerHTML={{ __html: post.html }} />
        <hr
          style={{
            marginBottom: rhythm(1),
          }}
        />
        

        <ul 
          className={styles.nextPrevious}
        >
          <li>
            {previous && (
              <Link to={previous.frontmatter.path} rel="prev">
                ← {previous.frontmatter.title}
              </Link>
            )}
          </li>
          <li>
            {next && (
              <Link to={next.frontmatter.path} rel="next">
                {next.frontmatter.title} →
              </Link>
            )}
          </li>
        </ul>
      </div>
      </div>
    )
  }
}

export default BlogPostTemplate

export const pageQuery = graphql`
  query BlogPostBySlug($slug: String!) {
    site {
      siteMetadata {
        title
        author
      }
    }
    markdownRemark(fields: { slug: { eq: $slug } }) {
      id
      excerpt(pruneLength: 160)
      html
      frontmatter {
        title
        date(formatString: "MMMM DD, YYYY")
      }
    }
  }
`