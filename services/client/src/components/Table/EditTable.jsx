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

import editTableStyle from "assets/jss/material-dashboard-react/editTableStyle";
import {Edit, Close, Restore} from "@material-ui/icons";

function EditTable({...props}) {
  const {classes, tableHead, tableData, tableHeaderColor, handleRemove, handleEdit, handleRestore} = props;
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
          {tableData.map((row, key) => {
            return (
              <TableRow key={key}>
                {row.data ? row.data.map((prop, key) => {
                  return (
                    <TableCell
                      className={row.deleted ? classes.tableCell + " " + classes.tableCellDeleted : classes.tableCell}
                      key={key}>
                      {prop}
                    </TableCell>
                  );
                }) : null}
                <TableCell
                  className={row.deleted ? classes.tableActions + " " + classes.tableCellDeleted : classes.tableActions}>
                  {row.deleted
                    ?
                    <Tooltip
                      id="tooltip-top"
                      title="Restore"
                      placement="top"
                      classes={{tooltip: classes.tooltip}}
                    >
                      <IconButton
                        aria-label="Restore"
                        className={classes.tableActionButton}
                        onClick={() => handleRestore(_.toInteger(row.data[0]))}
                      >
                        <Restore
                          className={
                            classes.tableActionButtonIcon + " " + classes.restore
                          }
                        />
                      </IconButton>
                    </Tooltip>
                    :
                    <div>
                      <Tooltip
                        id="tooltip-top"
                        title="Edit"
                        placement="top"
                        classes={{tooltip: classes.tooltip}}
                      >
                        <IconButton
                          aria-label="Edit"
                          className={classes.tableActionButton}
                          onClick={() => handleEdit(_.toInteger(row.data[0]))}
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
                          onClick={() => handleRemove(_.toInteger(row.data[0]))}
                        >
                          <Close
                            className={
                              classes.tableActionButtonIcon + " " + classes.close
                            }
                          />
                        </IconButton>
                      </Tooltip>
                    </div>
                  }
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
  tableData: PropTypes.arrayOf(PropTypes.shape({
    deleted: PropTypes.bool,
    data: PropTypes.arrayOf(PropTypes.string)
  }))
};

export default withStyles(editTableStyle)(EditTable);
