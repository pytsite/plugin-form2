import PropTypes from 'prop-types';
import React from 'react';
import ReactDOM from "react-dom";
import httpApi from '@pytsite/http-api';
import {createWidget} from '@pytsite/widget2';

class Form extends React.Component {
    static propTypes = {
        actionUrl: PropTypes.string.isRequired,
        getWidgetsPath: PropTypes.string.isRequired,
        method: PropTypes.string,
        steps: PropTypes.number.isRequired,
        submitPath: PropTypes.string.isRequired,
        uid: PropTypes.string.isRequired,
    };

    constructor(props) {
        super(props);

        this.state = {
            error: null,
            step: 0,
            widgets: [],
            widgetsValues: {},
        };

        this._onWidgetChange = this._onWidgetChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }

    _onWidgetChange(uid, e) {
        if (e.target.hasOwnProperty('value')) {
            const v = {};
            v[uid] = e.target.value;

            this.setState({
                widgetsValues: Object.assign({}, this.state.widgetsValues, v)
            })
        }
    }

    _getWidgets() {
        const endpoint = this.props.getWidgetsPath.replace('<uid>', this.props.uid).replace('<step>', this.state.step);

        httpApi.get(endpoint).then(r => {
            const widgets = [];

            r.forEach(wData => {
                wData.props.key = wData.props.id;
                wData.props.onChange = this._onWidgetChange;

                const widget = createWidget(wData['cid'], wData['props']);

                // Remember initial value of  the widget
                if (widget.props.hasOwnProperty('value')) {
                    const v = {};
                    v[widget.props.id] = widget.props.value;
                    this.setState({
                        widgetsValues: Object.assign({}, this.state.widgetsValues, v)
                    });
                }

                widgets.push(widget);
            });

            this.setState({widgets: widgets});
        });
    }

    onSubmit(e) {
        const endpoint = this.props.submitPath.replace('<uid>', this.props.uid).replace('<step>', this.state.step);

        e.preventDefault();

        httpApi.post(endpoint, this.state.widgetsValues).then(r => {
            if (this.props.actionUrl !== '#') {
                window.location.href = this.props.actionUrl;
            }
        }).catch(err => {
            if (err.hasOwnProperty('responseJSON') && err.responseJSON.error) {
                this.setState({error: err.responseJSON.error});
            }
        });

    }

    componentDidMount() {
        this._getWidgets();
    }

    render() {
        return (
            <form action={this.props.actionUrl}
                  id={this.props.uid}
                  onSubmit={this.onSubmit}
            >
                {this.state.error && (
                    <div className={'form-error'}>{this.state.error}</div>
                )}
                {this.state.widgets}
            </form>
        );
    }
}

document.querySelectorAll('.pytsite-form2-container').forEach(wrapper => {
    const form = <Form
        actionUrl={wrapper.getAttribute('data-action-url')}
        getWidgetsPath={wrapper.getAttribute('data-get-widgets-path')}
        steps={parseInt(wrapper.getAttribute('data-steps'))}
        submitPath={wrapper.getAttribute('data-submit-path')}
        uid={wrapper.getAttribute('data-uid')}
    />;

    ReactDOM.render(form, wrapper);
});
