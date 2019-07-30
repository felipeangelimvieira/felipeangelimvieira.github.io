import React from "react"
import Header from '../components/Header';
import { Link, graphql } from "gatsby"
import { rhythm } from "../utils/typography"
import styles from '../styles/blog.module.css'
import photo from '../assets/photo-about.png'
import shape from '../assets/shape.svg';
import shapeRed from '../assets/shapeRed.svg';




class BlogIndex extends React.Component {


  render() {
    const { data } = this.props
    const siteTitle = data.site.siteMetadata.title
    const posts = data.allMarkdownRemark.edges

    return (
      
      <div className={styles.body}>
      <Header />
      <img className={styles.backgroundShape} style={{top: -15 + '%',
                                                      left: -15 + '%'}} 
                                                      src={shape}></img>
      <img className={styles.backgroundShape} style={{top: -15 + '%',
                                                      right: 0 + '%'}} 
                                                      src={shapeRed}></img>
      <div className={styles.container}>
        <div className={styles.blankdiv}>
        
        
        </div>

        <div className={styles.containerBlogDescription}>
        <div className={styles.imageContainer}>
        <img src={photo} className={styles.profilePhoto}></img>
        </div>
        <div className={styles.descriptionText}>
        <h1 className={styles.blogTitle}> Paper summaries & Data</h1>
        <h4> A blog about data and cutting-edge machine learning technology</h4>
        </div>
        </div>
        <div className = {styles.postList}>
        {posts.map(({ node }) => {
          const title = node.frontmatter.title || node.fields.slug
          return (
            <div key={node.fields.slug}>
              <h3
                style={{
                  marginBottom: rhythm(1 / 4),
                }}
              >
                <Link className={styles.link} to={node.frontmatter.path}>
                  <h1 className={styles.title}>
                  {title}
                  </h1>
                </Link>
              </h3>
              <small>{node.frontmatter.date}</small>
              <p
                dangerouslySetInnerHTML={{
                  __html: node.frontmatter.description || node.excerpt,
                }}
              />
            </div>
          )
        })}
        </div>
    </div> 

    </div>
    )
  }
}

export default BlogIndex

export const pageQuery = graphql`
  query {
    site {
      siteMetadata {
        title
      }
    }
    allMarkdownRemark(sort: { fields: [frontmatter___date], order: DESC }) {
      edges {
        node {
          excerpt
          fields {
            slug
          }
          frontmatter {
            path
            date(formatString: "MMMM DD, YYYY")
            title
            description
          }
        }
      }
    }
  }
`