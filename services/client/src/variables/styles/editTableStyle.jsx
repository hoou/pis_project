// ##############################
// // // Table styles
// #############################

import {
  warningColor,
  primaryColor,
  dangerColor,
  successColor,
  infoColor,
  roseColor,
  grayColor,
  defaultFont
} from "variables/styles";

const tableStyle = theme => ({
  warningTableHeader: {
    color: warningColor
  },
  primaryTableHeader: {
    color: primaryColor
  },
  dangerTableHeader: {
    color: dangerColor
  },
  successTableHeader: {
    color: successColor
  },
  infoTableHeader: {
    color: infoColor
  },
  roseTableHeader: {
    color: roseColor
  },
  grayTableHeader: {
    color: grayColor
  },
  table: {
    marginBottom: "0",
    width: "100%",
    maxWidth: "100%",
    backgroundColor: "transparent",
    borderSpacing: "0",
    borderCollapse: "collapse"
  },
  tableHeadCell: {
    color: "inherit",
    ...defaultFont,
    fontSize: "1em"
  },
  tableCell: {
    ...defaultFont,
    lineHeight: "1.42857143",
    padding: "12px 8px",
    verticalAlign: "middle"
  },
  tableResponsive: {
    width: "100%",
    marginTop: theme.spacing.unit * 3,
    overflowX: "auto"
  },
  tableActions: {
    // display: "flex",
    padding: "12px 8px !important",
    verticalAlign: "middle"
  },
  tooltip: {
    padding: "10px 15px",
    minWidth: "130px",
    color: "#555555",
    lineHeight: "1.7em",
    background: "#FFFFFF",
    border: "none",
    borderRadius: "3px",
    boxShadow:
      "0 8px 10px 1px rgba(0, 0, 0, 0.14), 0 3px 14px 2px rgba(0, 0, 0, 0.12), 0 5px 5px -3px rgba(0, 0, 0, 0.2)",
    maxWidth: "200px",
    textAlign: "center",
    fontFamily: '"Helvetica Neue",Helvetica,Arial,sans-serif',
    fontSize: "12px",
    fontStyle: "normal",
    fontWeight: "400",
    textShadow: "none",
    textTransform: "none",
    letterSpacing: "normal",
    wordBreak: "normal",
    wordSpacing: "normal",
    wordWrap: "normal",
    whiteSpace: "normal",
    lineBreak: "auto"
  },
  tableActionButton: {
    width: "27px",
    height: "27px"
  },
  tableActionButtonIcon: {
    width: "20px",
    height: "20px"
  },
  edit: {
    backgroundColor: "transparent",
    color: primaryColor,
    boxShadow: "none"
  },
  close: {
    backgroundColor: "transparent",
    color: dangerColor,
    boxShadow: "none"
  }
});

export default tableStyle;
