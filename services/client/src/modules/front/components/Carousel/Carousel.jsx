import React, {Component} from 'react';
import SwipeableViews from 'react-swipeable-views';
import {autoPlay} from 'react-swipeable-views-utils';
import Pagination from './Pagination';
import SupportTouch from './SupportTouch';
import image1 from "modules/front/assets/img/carousel/1.jpg"
import image2 from "modules/front/assets/img/carousel/2.jpg"
import image3 from "modules/front/assets/img/carousel/3.jpg"
import {withStyles} from "material-ui";
import * as classnames from "classnames";

const AutoPlaySwipeableViews = autoPlay(SwipeableViews);

const styles = () => ({
  root: {
    position: 'relative',
    marginBottom: 15
  },
  slide: {
    height: 600,
    color: '#fff',
    overflow: "hidden",
    position: "relative"
  },
  slide1: {
    backgroundColor: '#FEA900',
  },
  slide2: {
    backgroundColor: '#B3DC4A',
  },
  slide3: {
    backgroundColor: '#6AC0FF',
  },
  slideImg: {
    position: "absolute",
    top: "50%",
    width: "100%",
    height: "auto",
    marginTop: -550
  }
});

class DemoAutoPlay extends Component {
  state = {
    index: 0,
  };

  handleChangeIndex = index => {
    this.setState({
      index,
    });
  };

  render() {
    const {index} = this.state;
    const {classes} = this.props;

    return (
      <SupportTouch>
        <div className={classes.root}>
          <AutoPlaySwipeableViews interval={5000} index={index} onChangeIndex={this.handleChangeIndex}>
            <div className={classnames(classes.slide, classes.slide1)}>
              <img className={classes.slideImg} src={image1}/>
            </div>
            <div className={classnames(classes.slide, classes.slide2)}>
              <img className={classes.slideImg} src={image2}/>
            </div>
            <div className={classnames(classes.slide, classes.slide3)}>
              <img className={classes.slideImg} src={image3}/>
            </div>
          </AutoPlaySwipeableViews>
          <Pagination dots={3} index={index} onChangeIndex={this.handleChangeIndex}/>
        </div>
      </SupportTouch>
    );
  }
}

export default withStyles(styles)(DemoAutoPlay);