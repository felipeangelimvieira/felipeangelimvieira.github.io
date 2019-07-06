import React from 'react';
import backgroundImage from '../assets/background-crop1.jpg';
import arrow from '../assets/baseline_keyboard_arrow_down_white_48dp.png'
import styles from '../styles/background-image.module.css';
import Img from 'gatsby-image';

export default props => { 

    return (

        <div className={styles.container}>
            <Img fluid={props.data.imageOne.childImageSharp.fluid} />
            <div className = {styles.imageContentContainer}>
            <div className = {styles.imageTextContainer}>
            <p className={styles.text}>Hello, it's Felipe.</p>
            <p className={styles.mainMessage}>I'm an engineering student.</p>
            <p className={styles.text}>I use data and maths to solve problems.</p>
            </div>
            <div className={styles.arrowContainer}>
                <a href="/#about"><img src={arrow} className = {styles.arrow}/></a>
            </div>
            
            </div>
            
        </div>
)}

