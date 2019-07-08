import React from 'react';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import classes from '../styles/projects.module.css';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

export default function() {


    return (
        <div className = {classes.container}>
            <h1>Projects</h1>
        <Card className={classes.card}>
      <CardContent>
        <Typography className={classes.theme} color="textSecondary" gutterBottom>
          Full-stack developer
        </Typography>
        <Typography className={classes.title} variant="h5" component="h2">
          Como vota, deputado?
        </Typography>
        <div className = {classes.descriptionContainer}>
        <Typography className={classes.description} variant="body2" component="p">
          An open-source website for citizens to follow up congressmen after elections, and 
          see what they're voting for. I'm using React.js, Node.js and MongoDB.
          This project is currently under development.
        </Typography>
        </div>
      </CardContent>
      <CardActions>
        <Button size="small">Learn More</Button>
      </CardActions>
    </Card>

    <Card className={classes.card}>
      <CardContent>
        <Typography className={classes.theme} color="textSecondary" gutterBottom>
          Full Stack developer
        </Typography>
        <Typography className={classes.title} variant="h5" component="h2">
          Parktout
        </Typography>
        <div className = {classes.descriptionContainer}>
        <Typography className={classes.description} variant="body2" component="p">
          An android application that provides information about more than 1000 parkings in Lyon, France.
          I managed a team of 5 members and participated on data pre-processing for parking availability prediction.
        </Typography>
        </div>
      </CardContent>
      <CardActions>
        <Button size="small">Learn More</Button>
      </CardActions>
    </Card>
    </div>
    )
}