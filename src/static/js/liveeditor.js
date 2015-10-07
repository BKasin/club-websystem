var sv_textarea;
var sv_preview;
var sv_changedindicator;
var sv_changed = false;
var sv_refreshdelay = 1000;
var sv_timer;

$(function() {
  sv_textarea = $('#sv-textarea')
  sv_preview = $('#sv-preview')
  sv_submitbutton = document.getElementById('sv-submitbutton')

  // Begin auto-resizing of our textarea
  $(document).ready(function () {
    autosize(sv_textarea);
  });

  // Initial render
  sv_render();

  // Render on each key press
  sv_textarea.bind('keyup', function() {
    if (sv_timer) clearTimeout(sv_timer);
    sv_timer = setTimeout(function() {
      sv_set_changed();
      sv_render();
    }, sv_refreshdelay);
  });

  // Warn user before closing window
  $(window).bind('beforeunload', function() {
    if (sv_changed) {
      return 'If you close this page, your changes will be lost. Are you sure?';
    }
  });
});

function sv_render() {
  sv_preview.html(markdown.toHTML(sv_textarea.val()));
}

function sv_set_changed() {
  if (!sv_changed) {
    sv_changed = true;
    sv_submitbutton.style.display='inline';
  }
  sv_timer = null;
}
