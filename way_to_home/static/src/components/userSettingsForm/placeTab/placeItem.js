import React from 'react';

import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import Modal from '@material-ui/core/Modal';
import Chip from '@material-ui/core/Chip'
import Button from '@material-ui/core/Button'
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

import PlaceForm from './placeForm';
import './place.css'


class PlaceItem extends React.Component {

    state = {
        openDeleteModal: false,
        openEditModel: false,
        text: this.props.place.name
    };

    onClickDelete = () => {
        this.setState({openDeleteModal: true});
    };

    modalDeleteClose = () => {
        this.setState({openDeleteModal: false});
    };

    onClickEdit = () => {
        this.setState({openEditModel: true});
    };

    modalEditClose = () => {
        this.setState({openEditModel: false});
    };

    hoverOn = () => {
        this.setState({
            text: this.props.place.address
        });
    };

    hoverOff = () => {
        this.setState({
            text: this.props.place.name
        });
    };

    render(){
        let {place} = this.props;

        return (
            <div>
                <Chip
                    className='placeItem'
                    color='primary'
                    label={this.state.text || 'Без назви'}
                    variant='outlined'
                    onClick={this.onClickEdit}
                    onMouseEnter={this.hoverOn}
                    onMouseLeave={this.hoverOff}
                        />
                <IconButton className='removeButton' color='secondary'  onClick={this.onClickDelete}>
                    <DeleteIcon />
                </IconButton>

                <Modal
                    open={this.state.openEditModel}
                    onClose={this.modalEditClose}
                    disableAutoFocus='True'>
                    <PlaceForm
                        updatePlace={this.props.updatePlace}
                        form_type='Зберегти'
                        place={place}
                        close={this.modalEditClose} />
                </Modal>

                <Dialog
                  open={this.state.openDeleteModal}
                  aria-labelledby="alert-dialog-title"
                  aria-describedby="alert-dialog-description"
                >
                  <DialogTitle id="alert-dialog-title">{"Видалити місце ?"}</DialogTitle>
                  <DialogContent>
                    <DialogContentText id="alert-dialog-description">
                      Ви впевнені що хочете видалити місце?
                    </DialogContentText>
                  </DialogContent>
                  <DialogActions>
                    <Button
                        onClick={this.modalDeleteClose}
                        variant="outlined"
                        color="primary"
                    >
                      Скасувати
                    </Button>
                    <Button
                        onClick={() => this.props.deleteButton(this.props.place.id)}
                        variant="outlined"
                        color="primary"
                        autoFocus
                    >
                      Видалити
                    </Button>
                  </DialogActions>
                </Dialog>
            </div>
        );
    };
}

export default PlaceItem;
