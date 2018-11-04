  function renderTable(dicts, tableHeaders, tableProperties, viewUrlBase, viewUrlProperty, tableElementId) {
    var generatedTableRows = generateTableRows(dicts, tableProperties, viewUrlBase, viewUrlProperty);
    var tableHtml = "<table class='table'>"
        + renderTableHeaders(tableHeaders)
        + renderTableRows(generatedTableRows)
        + "</table>";
    document.getElementById(tableElementId).innerHTML = tableHtml;
  }

  function generateTableRows(dicts, tableProperties, viewUrlBase, viewUrlProperty) {
    var ret = [];
    for (i in dicts) {
      var tableRow = [];
      var dict = dicts[i];
      for (j in tableProperties) {
        if (j == 0) {
          tableRow.push("<a href='" + viewUrlBase + dict[viewUrlProperty] + "'>" + dict[tableProperties[j]] + "</a>");
        } else {
          tableRow.push(dict[tableProperties[j]]);
        }
      }
      ret.push(tableRow);
    }
    return ret;
  }

  function renderTableHeaders(headers) {
    return "<tr><th>" + headers.join("</th><th>") + "</th></tr>";
  }

  function renderTableRows(rows) {
    var ret = "";
    for (i in rows) {
      var row = rows[i];
      ret += renderTableRow(row);
    }
    return ret;
  }

  function renderTableRow(cols) {
    return "<tr><td>" + cols.join("</td><td>") + "</td></tr>";
  }

  function getValue(elementId) {
    return document.getElementById(elementId).value.toLowerCase();
  }
