import React from "react";
import _ from "lodash";
import {
  withStyles,
  Table,
  TableHead,
  TableRow,
  TableBody,
  TableCell, Tooltip, IconButton
} from "material-ui";

import PropTypes from "prop-types";

import editTableStyle from "variables/styles/editTableStyle";

import {Close, Edit} from "material-ui-icons";


function EditTable({...props}) {
  const {classes, tableHead, tableData, tableHeaderColor, handleRemove} = props;
  return (
    <div className={classes.tableResponsive}>
      <Table className={classes.table}>
        {tableHead !== undefined ? (
          <TableHead className={classes[tableHeaderColor + "TableHeader"]}>
            <TableRow>
              {tableHead.map((prop, key) => {
                return (
                  <TableCell
                    className={classes.tableCell + " " + classes.tableHeadCell}
                    key={key}
                  >
                    {prop}
                  </TableCell>
                );
              })}
              <TableCell
                className={classes.tableCell + " " + classes.tableHeadCell}
                key="actions"
              >
                {"Actions"}
              </TableCell>
            </TableRow>
          </TableHead>
        ) : null}
        <TableBody>
          {tableData.map((prop, key) => {
            return (
              <TableRow key={key}>
                {prop.map((prop, key) => {
                  return (
                    <TableCell className={classes.tableCell} key={key}>
                      {prop}
                    </TableCell>
                  );
                })}
                <TableCell className={classes.tableActions}>
                  <Tooltip
                    id="tooltip-top"
                    title="Edit"
                    placement="top"
                    classes={{tooltip: classes.tooltip}}
                  >
                    <IconButton
                      aria-label="Edit"
                      className={classes.tableActionButton}
                    >
                      <Edit
                        className={
                          classes.tableActionButtonIcon + " " + classes.edit
                        }
                      />
                    </IconButton>
                  </Tooltip>
                  <Tooltip
                    id="tooltip-top-start"
                    title="Remove"
                    placement="top"
                    classes={{tooltip: classes.tooltip}}
                  >
                    <IconButton
                      aria-label="Close"
                      className={classes.tableActionButton}
                      onClick={() => handleRemove(_.toInteger(prop[0]))}
                    >
                      <Close
                        className={
                          classes.tableActionButtonIcon + " " + classes.close
                        }
                      />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}

EditTable.defaultProps = {
  tableHeaderColor: "gray"
};

EditTable.propTypes = {
  classes: PropTypes.object.isRequired,
  tableHeaderColor: PropTypes.oneOf([
    "warning",
    "primary",
    "danger",
    "success",
    "info",
    "rose",
    "gray"
  ]),
  tableHead: PropTypes.arrayOf(PropTypes.string),
  tableData: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.string))
};

export default withStyles(editTableStyle)(EditTable);
