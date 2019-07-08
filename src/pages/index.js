import React from "react";
import Landing from "../components/landing";
import About from '../components/about';
import Timeline from '../components/timeline';
import styles from '../styles/global.css';
import { graphql } from 'gatsby';


export default ({data}) => (<div className={styles.body}>
        <Landing data={data}/>
        <About />
        <Timeline/>
</div>)




export const query = graphql`
query {
    imageOne: file(relativePath: { eq: "background-crop1.jpg" }) {
      childImageSharp {
        fluid(maxWidth: 3000) {
          base64
          tracedSVG
          aspectRatio
          src
          srcSet
          srcWebp
          srcSetWebp
          sizes
          originalImg
          originalName
        }
      }
    }
  }
`