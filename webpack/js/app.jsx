import PropTypes from 'prop-types';
import React from 'react';
import ReactDOM from 'react-dom';

require('bootstrap');

class PyPIBox extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      latestRelease: null,
      downloadInfo: null
    };
  }

  componentDidMount() {
    $.ajax({
      method: 'GET',
      url: 'https://pypi.org/pypi/' + this.props.packageName + '/json',
      crossDomain: true
    }).then((data) => {
      this.setState({
        latestRelease: data.info.version,
        downloadInfo: data.info.downloads
      });
    });
  }

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
      </div>
    );
  }
}

PyPIBox.propTypes = {
  packageName: PropTypes.string
};

function initPyPIStats() {
  $('.pypi-box').each(function() {
    ReactDOM.render(<PyPIBox packageName={$(this).data('pypi')} />, this);
  });
}

$(function() {
  initPyPIStats();
});
