import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from 'material-ui/styles';
import Card, {CardHeader, CardMedia, CardContent} from 'material-ui/Card';
import IconButton from 'material-ui/IconButton';
import Typography from 'material-ui/Typography';
import red from 'material-ui/colors/red';

import placeholder from "modules/front/assets/img/placeholder.png"
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
    const {classes, title, price, description, count, images} = this.props;

    return (
      <div>
        <Card className={classes.card}>
          <CardHeader
            classes={{
              title: classes.cardHeaderTitle,
              subheader: classes.cardSubHeader
            }}
            title={title}
            subheader={price + " EUR"}
            action={
              <IconButton aria-label="Add to cart">
                <AddShoppingCart/>
              </IconButton>
            }
          />
          <CardMedia
            className={classes.media}
            image={images[0] ? images[0].url : placeholder}
            title={title}
          />
          <CardContent>
            <Typography variant="caption" align="right" noWrap={true}>
              Na sklade: {count}
            </Typography>
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