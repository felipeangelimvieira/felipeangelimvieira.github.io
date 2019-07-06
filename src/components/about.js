import React from 'react';
import photo from '../assets/photo-about.png'
import styles from '../styles/about.module.css';

export default () => (

        <div id="about" className = {styles.container}>
            <div className = {styles.imageContainer}>
                <img className={styles.photo} src={photo}></img>
            </div>
            <div className={styles.aboutTextContainer}>
                <h2 className={styles.aboutText}>About me</h2>
            </div>
            
            <div className={styles.descriptionContainer}>
            <p className={styles.description}>I'm a double-degree engineering student at
             École Centrale de Lyon and Federal University of Rio de Janeiro, currently finishing my studies
             in Brazil. I'm always reading the latest scientific papers on Machine Learning to keep updated about
             cutting-edge technology. Feel free to contact me if you're interested in working together on a project
             or needing help with some AI product.
            </p>
            </div>
            
            <p >I'm machine learning engineering student</p>
            <p >I use data and maths to solve problems</p>
        </div>
)