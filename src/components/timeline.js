import React from 'react';
import { StyleRoot } from 'radium'
import { VerticalTimeline, VerticalTimelineElement }  from 'react-vertical-timeline-component';
import 'react-vertical-timeline-component/style.min.css';
import {School, Work, Description } from '@material-ui/icons';

import timelineData from '../assets/timeline-data';


function classNameMap(x)
{
    const className = {
                    "work" : "vertical-timeline-element--work",
                    "education" : "vertical-timeline-element--education"
                    }

    var classname = className[x];
    if (!classname){
        return "vertical-timeline-element--education"
    }
    return classname
}

function iconMap(x) {

    const corresp = {
        "work" : <Work/>,
        "educaton" : <School/>,
        "publication" : <Description />
    };

    return corresp[x];

}

function parseElement(x) {

    return (
    <VerticalTimelineElement
    className={ classNameMap(x.type) }
    date={x.date}
    iconStyle={{ background: 'rgb(33, 150, 243)', color: '#fff', textAlign: 'center'}}
    icon= {iconMap(x.type)} >
    <h3 className="vertical-timeline-element-title">{x.title}</h3>
    <h4 className="vertical-timeline-element-subtitle">{x.subtitle}</h4>
    <p>
      {x.description}
    </p>
  </VerticalTimelineElement>
    )
}

export default () => (

<div>
<div style = {{textAlign : "center"}}>
    <h1>Experience</h1>
</div>
<VerticalTimeline>
<VerticalTimelineElement
    className="vertical-timeline-element--work"
    date="May 2019 - present"
    iconStyle={{ background: 'rgb(33, 150, 243)', color: '#fff' }}
    icon={<Work />}
  >
    <h3 className="vertical-timeline-element-title">Data Analyst</h3>
    <h4 className="vertical-timeline-element-subtitle">Brasa (Brazilian Student Association)</h4>
    <p>
        As a member of Tech team, I manage the SQL databases and build BI dashboards.
    </p>
</VerticalTimelineElement>

<VerticalTimelineElement
    className="vertical-timeline-element--work"
    date="Nov 2018 - April 2019"
    iconStyle={{ background: 'rgb(33, 150, 243)', color: '#fff' }}
    icon={<Work />}
  >
    <h3 className="vertical-timeline-element-title">Data Science Intern</h3>
    <h4 className="vertical-timeline-element-subtitle">Amadeus - Nice, France</h4>
    <p>
        Development of clustering algorithm and NLP model
        that could identify flights' cancellation reasons from text and historical data.
    </p>
  </VerticalTimelineElement>

  <VerticalTimelineElement
    className="vertical-timeline-element--work"
    date="May 2018 - Nov 2018"
    iconStyle={{ background: 'rgb(33, 150, 243)', color: '#fff' }}
    icon={<Work />}
  >
    <h3 className="vertical-timeline-element-title">Machine Learning Intern</h3>
    <h4 className="vertical-timeline-element-subtitle">Dassault Systèmes - Paris, France</h4>
    <p>
        Enhanced 3D object classification algorithms by implementing cutting-edge technology.
        At the end of my internship, I had reduced the classification error by more than 60%.
    </p>
  </VerticalTimelineElement>

  <VerticalTimelineElement
    className="vertical-timeline-element--work"
    date="Oct 2015 - Jul 2016"
    iconStyle={{ background: 'rgb(33, 150, 243)', color: '#fff' }}
    icon={<Work />}
  >
    <h3 className="vertical-timeline-element-title">Co-founder and Powertrain manager</h3>
    <h4 className="vertical-timeline-element-subtitle">Minerva eRacing - Rio de Janeiro, Brazil</h4>
    <p>
        I co-founded and managed the powertrain team of the first Formula SAE Electric
        team of my University.
    </p>
  </VerticalTimelineElement>

</VerticalTimeline>

<div style = {{textAlign : "center"}}>
    <h1>Education</h1>
</div>

<VerticalTimeline>
<VerticalTimelineElement
    className="vertical-timeline-element--work"
    date="2016 - 2018"
    iconStyle={{ background: 'rgb(33, 150, 243)', color: '#fff' }}
    icon={<School />}
  >
    <h3 className="vertical-timeline-element-title">École Centrale de Lyon</h3>
    <h4 className="vertical-timeline-element-subtitle">Generalist Engineering</h4>
    <p>
        Double-degree program, awarded an Eiffel Excellence Scholarship.
    </p>
</VerticalTimelineElement>

<VerticalTimelineElement
    className="vertical-timeline-element--work"
    date="2014 - 2020"
    iconStyle={{ background: 'rgb(33, 150, 243)', color: '#fff' }}
    icon={<School />}
  >
    <h3 className="vertical-timeline-element-title">Federal University of Rio de Janeiro (UFRJ)</h3>
    <h4 className="vertical-timeline-element-subtitle">Mechanical Engineering</h4>

</VerticalTimelineElement>

</VerticalTimeline>


</div>
)