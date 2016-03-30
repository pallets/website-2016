import React from 'react';
import ReactDOM from 'react-dom';
import {abbrRoundNumber} from './utils';

require('bootstrap');

const PyPIBox = React.createClass({
  propTypes: {
    packageName: React.PropTypes.string
  },

  getInitialState() {
    return {
      latestRelease: null,
      downloadInfo: null
    }
  },

  componentDidMount() {
    $.ajax({
      method: 'GET',
      url: 'https://pypi.python.org/pypi/' + this.props.packageName + '/json',
      crossDomain: true
    }).then((data) => {
      console.log(data);
      this.setState({
        latestRelease: data.info.version,
        downloadInfo: data.info.downloads
      });
    });
  },

  render() {
    if (!this.state.downloadInfo) {
      return null;
    }
    return (
      <div>
        <hr/>
        <h3>Latest Release</h3>
        <p><strong>Version:</strong>{' '}
          {this.state.latestRelease}</p>
        <h3>Downloads</h3>
        <p><strong>Last month:</strong>{' '}
          {abbrRoundNumber(this.state.downloadInfo.last_month)}</p>
        <p><strong>Last week:</strong>{' '}
          {abbrRoundNumber(this.state.downloadInfo.last_week)}</p>
      </div>
    );
  }
});

function initPyPIStats() {
  $('.pypi-box').each(function() {
    ReactDOM.render(<PyPIBox packageName={$(this).data('pypi')} />, this);
  });
}

$(function() {
  initPyPIStats();
});
