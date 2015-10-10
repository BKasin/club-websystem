"use strict";

/* Requires jQuery ($ global) */
/* Requires lodash (_ global) */

var sv_textarea, sv_preview, sv_submitbutton, sv_datatypedropdown;
var sv_cur_datatype = '';
var sv_changed = false;

var commonmark = window.commonmark;
var writer = new commonmark.HtmlRenderer({ sourcepos: true });
var reader = new commonmark.Parser();

function sv_render_initial() {
  switch(sv_cur_datatype) {
  case 'md':
    var parsed = reader.parse(sv_textarea.val());
    if (parsed === undefined) return;
    sv_preview.html(writer.render(parsed));
    sv_preview.css('white-space', '');
    break;
  case 'htm':
    sv_preview.html(sv_textarea.val());
    sv_preview.css('white-space', '');
    break;
  case 'txt':
    sv_preview.text(sv_textarea.val());
    sv_preview.css('white-space', 'pre-wrap');
    break;
  default:
    sv_preview.html('');
  }
}
function sv_render() {
  sv_render_initial();
  sv_hilight_selection();
  sv_changed = true;
}

// Function to determine which paragraph in the source the cursor is at,
//   and hilight the same paragraph in the HTML Preview
function sv_hilight_selection() {
  if (sv_cur_datatype=='md') {
    var cursorPos = sv_textarea.prop("selectionStart");
    // now count newline up to this pos
    var textval = sv_textarea.val();
    var lineNumber = 1;
    for (var i = 0; i < cursorPos; i++) {
      if (textval.charAt(i) === '\n') {
        lineNumber++;
      }
    }
    var elt = $("#sv-preview [data-sourcepos^='" + lineNumber + ":']").last();
    sv_hide_selection();
    if (elt.length > 0) {
      elt.addClass("selected");
    }
  }
}
function sv_hide_selection() {
  $("#sv-preview .selected").removeClass("selected");
}

function sv_update_datatype() {
  sv_cur_datatype = sv_datatypedropdown.val();
}

$(function() {
  sv_textarea = $('#sv-textarea')
  sv_preview = $('#sv-preview')
  sv_submitbutton = $('#sv-submitbutton')
  sv_datatypedropdown = $('#id_datatype')

  // Begin auto-resizing of our textarea
  $(document).ready(function () {
    autosize(sv_textarea);
  });

  // Initial render
  sv_update_datatype();
  sv_render_initial();

  // Register events
  sv_datatypedropdown.on('input', function() {
    sv_update_datatype();
    sv_render();
  });
  sv_textarea.on('input',
    // Debounce causes sv_render to called 300ms after the user
    // stops typing, or each 1000ms during continuous typing
    _.debounce(sv_render, 300, { maxWait: 1000 })
  );
  sv_textarea.on('keydown click focus',
    // Debounce causes sv_hilight_selection to be called 300ms after the user
    //   stops moving the cursor, or each 1000ms during continuous movement
    _.debounce(sv_hilight_selection, 300, { maxWait: 1000})
  );
  sv_textarea.on('blur', sv_hide_selection);

  // Warn user before closing window
  $(window).on('beforeunload', function() {
    if (sv_changed) {
      return 'If you close this page, your changes will be lost. Are you sure?';
    }
  });
  sv_submitbutton.on('click', function() {
    $(window).off('beforeunload');
  });
});
