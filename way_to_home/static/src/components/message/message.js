
import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import ErrorIcon from '@material-ui/icons/Error';
import CloseIcon from '@material-ui/icons/Close';
import IconButton from '@material-ui/core/IconButton';
import Snackbar from '@material-ui/core/Snackbar';
import SnackbarContent from '@material-ui/core/SnackbarContent';
import { withStyles } from '@material-ui/core/styles';


const styles1 = theme => ({
    error: {
        backgroundColor: theme.palette.error.dark,
    },
    icon: {
        fontSize: 20,
    },
    iconVariant: {
        opacity: 0.9,
        marginRight: theme.spacing.unit,
    },
    message: {
        display: 'flex',
        alignItems: 'center',
    },
});

function MySnackbarContent(props) {
    const { classes, message, onClose} = props;
    return (
        <SnackbarContent
            className={classes.error}
            message={
                <span className={classes.message}>
          <ErrorIcon className={classNames(classes.icon, classes.iconVariant)} />
                    {message}
        </span>
            }
            action={[
                <IconButton
                    color="inherit"
                    onClick={onClose}
                >
                    <CloseIcon className={classes.icon} />
                </IconButton>,
            ]}
        />
    );
}

MySnackbarContent.propTypes = {
    message: PropTypes.node.isRequired,
    onClose: PropTypes.func,
};

const MySnackbarContentWrapper = withStyles(styles1)(MySnackbarContent);


class CustomizedSnackbars extends React.Component {

    constructor(props){
        super(props)
        this.state = {
            open: true,
            message: this.props.message,
        };
    }

    handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        this.setState({ open: false });
        this.props.reset();
    };

    render() {
        return (
            <div>
                <Snackbar
                    anchorOrigin={{
                        vertical: 'bottom',
                        horizontal: 'right',
                    }}
                    open={this.state.open}
                    autoHideDuration={5000}
                    onClose={this.handleClose}
                >
                    <MySnackbarContentWrapper
                        key="close"
                        message={this.state.message}
                        onClose={this.handleClose}
                    />
                </Snackbar>
            </div>
        );
    }
}

export default CustomizedSnackbars;
