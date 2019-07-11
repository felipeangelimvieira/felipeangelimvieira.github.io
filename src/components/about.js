import React from 'react';
import photo from '../assets/photo-about.png'
import styles from '../styles/about.module.css';
import ScrollAnimation from 'react-animate-on-scroll';
import "animate.css/animate.min.css";

export default () => (

        <div id="about" className = {styles.container}>
            
            <div className = {styles.imageContainer}>
                <img className={styles.photo} src={photo}></img>
            </div>
            
            <ScrollAnimation animateIn="slideInUp" animateOnce={true} offset={500} duration={2}>
            <div className={styles.aboutTextContainer}>
                <h1 className={styles.aboutText}>About me</h1>
            </div>
            
            <div className={styles.descriptionContainer}>
            
            <p className={styles.description}>
             Hello, my name is Felipe Angelim. I'm currently
             in Brazil to finish a double-degree program between my Brazilian university
             (Federal University of Rio de Janeiro) and my French university (École Centrale
             de Lyon).
             I have work experience in Machine Learning and Data Science, 
             particularly Natural Language, Computer Vision and clustering, and I love
             reading the latest scientific papers to keep updated on cutting-edge
             technology.
            </p>
            <p>
            Aside from my academic and professional life, I believe that sports, sincere smiles and hanging out with friends are some
            of the pillars of a happy life.
            </p>
            <p>Feel free to contact me
             if you're needing help with some AI product
             or if you're interested in working together on a project.</p>
            </div>
            </ScrollAnimation>
            
        </div>
)