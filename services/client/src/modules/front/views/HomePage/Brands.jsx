import React from "react";
import {Card, CardMedia, Grid, withStyles} from "material-ui";
import Image from "material-ui-image"

import johndeere from "modules/front/assets/img/brands/johndeere_logo.png"
import newholland from "modules/front/assets/img/brands/newholland_logo.png"
import valtra from "modules/front/assets/img/brands/valtra_logo.png"
import zetor from "modules/front/assets/img/brands/zetor_logo.svg"

const styles = {
  root: {
    marginBottom: 50,
    marginTop: 50
  }
};

const Brands = (props) => {
  const {classes} = props;

  return (
    <Grid className={classes.root} container spacing={40} justify="center">
      <Grid item xs={12} sm={6} md={3} lg={2}>
        <Image color="none" src={johndeere}/>
      </Grid>
      <Grid item xs={12} sm={6} md={3} lg={2}>
        <Image color="none" src={newholland}/>
      </Grid>
      <Grid item xs={12} sm={6} md={3} lg={2}>
        <Image color="none" src={valtra}/>
      </Grid>
      <Grid item xs={12} sm={6} md={3} lg={2}>
        <Image color="none" src={zetor}/>
      </Grid>
    </Grid>
  )
};

export default withStyles(styles)(Brands);