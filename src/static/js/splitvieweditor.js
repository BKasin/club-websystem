"use strict";

/* Requires jQuery ($ global) */
/* Requires lodash (_ global) */

var sv_textarea;
var sv_preview;
var sv_submitbutton;
var sv_changed = false;

var commonmark = window.commonmark;
var writer = new commonmark.HtmlRenderer({ sourcepos: true });
var reader = new commonmark.Parser();

function sv_render_initial() {
  var parsed = reader.parse(sv_textarea.val());
  if (parsed === undefined) return;
  sv_preview.html(writer.render(parsed));
}
function sv_render() {
  sv_render_initial();
  sv_hilight_selection();
  if (!sv_changed) {
    // Show the submit button, since changed have been made
    sv_changed = true;
    sv_submitbutton.css('display', 'inline');
  }
}

// Function to determine which paragraph in the source the cursor is at,
//   and hilight the same paragraph in the HTML Preview
function sv_hilight_selection() {
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
  if (elt.length > 0) {
    $("#sv-preview .selected").removeClass("selected");
    elt.addClass("selected");
  }
}

$(function() {
  sv_textarea = $('#sv-textarea')
  sv_preview = $('#sv-preview')
  sv_submitbutton = $('#sv-submitbutton')

  // Begin auto-resizing of our textarea
  $(document).ready(function () {
    autosize(sv_textarea);
  });

  // Initial render
  sv_render_initial();

  sv_textarea.bind('input propertychange',
    // Debounce causes sv_render to called 300ms after the user
    // stops typing, or each 1000ms during continuous typing
    _.debounce(sv_render, 300, { maxWait: 1000 })
  );
  sv_textarea.on('keydown click focus',
    // Debounce causes sv_hilight_selection to be called 300ms after the user
    //   stops moving the cursor, or each 1000ms during continuous movement
    _.debounce(sv_hilight_selection, 300, { maxWait: 1000})
  );

  // Warn user before closing window
  $(window).bind('beforeunload', function() {
    if (sv_changed) {
      return 'If you close this page, your changes will be lost. Are you sure?';
    }
  });
});
