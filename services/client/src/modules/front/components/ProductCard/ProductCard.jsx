import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from 'material-ui/styles';
import Card, {CardHeader, CardMedia, CardContent, CardActions} from 'material-ui/Card';
import Collapse from 'material-ui/transitions/Collapse';
import IconButton from 'material-ui/IconButton';
import Typography from 'material-ui/Typography';
import red from 'material-ui/colors/red';

import traktorImage from "modules/front/assets/img/traktor.jpg"
import {AddShoppingCart} from "@material-ui/icons";

const styles = theme => ({
  card: {
    maxWidth: 400,
  },
  cardHeaderTitle: {
    fontSize: '1em'
  },
  cardSubHeader: {
    fontSize: '0.8em'
  },
  media: {
    height: 0,
    paddingTop: '56.25%', // 16:9
  },
  actions: {
    display: 'flex',
  },
  expand: {
    transform: 'rotate(0deg)',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
    marginLeft: 'auto',
  },
  expandOpen: {
    transform: 'rotate(180deg)',
  },
  avatar: {
    backgroundColor: red[500],
  },
});

class ProductCard extends React.Component {
  state = {expanded: false};
  render() {
    const {classes, title, price, description} = this.props;

    return (
      <div>
        <Card className={classes.card}>
          <CardHeader
            classes={{
              title: classes.cardHeaderTitle,
              subheader: classes.cardSubHeader
            }}
            title={title}
            subheader={price}
            action={
              <IconButton aria-label="Add to cart">
                <AddShoppingCart/>
              </IconButton>
            }
          />
          <CardMedia
            className={classes.media}
            image={traktorImage}
            title="Contemplative Reptile"
          />
          <CardContent>
            <Typography component="p" noWrap={true}>
              {description}
            </Typography>
          </CardContent>
        </Card>
      </div>
    );
  }
}

ProductCard.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ProductCard);