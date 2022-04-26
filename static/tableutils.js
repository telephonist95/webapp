function setItemType(tableid, typename)
{
    var tb = document.getElementById(tableid);
    if (tb) {
	rows = tb.rows;
	rowsCount = rows.length;
	for (r = 1; r < rowsCount; r++) {
	    rows[r].hidden = false;
	    cells = rows[r].cells;
	    if (cells[2].textContent != typename) {
		rows[r].hidden = true;
	    }
	}
    }
}
