#!/usr/bin/env python

# //******************************************************************************
# //
# //  rpnAstronomy.py
# //
# //  RPN command-line calculator astronomical operators
# //  copyright (c) 2019, Rick Gutleber (rickg@his.com)
# //
# //  License: GNU GPL 3.0 (see <http://www.gnu.org/licenses/gpl.html> for more
# //  information).
# //
# //  adapted from:
# //
# //  Javascript Lunar Eclipse Explorer
# //  Version 1.1 by Chris O'Byrne and Fred Espenak - 2014 Mar 18.
# //
# //  This code is being released under the terms of the GNU General Public
# //  License (http://www.gnu.org/copyleft/gpl.html) with the request
# //  that if you do improve on it or use it in your own site,
# //  please let us know at
# //  chris@obyrne.com  and  fred espenak (www.eclipsewise.com)    Thanks!
# //
# //  http://www.eclipsewise.com/lunar/JLEX/JLEX-index.html
# //
# //******************************************************************************

import ephem

//
// Observer constants -
// (0) North Latitude (radians)
// (1) West Longitude (radians)
// (2) Altitude (metres)
// (3) West time zone (hours)
// (4) index into the elements array for the eclipse in question
// (5) maximum eclipse type
//
var obsvconst = new Array();

//
// Eclipse circumstances
//  (0) Event type (p1=-3, u1=-2, u2=-1, mid=0, u3=1, u4=2, p4=3)
//  (1) t
//  (2) hour angle
//  (3) declination
//  (4) alt
//  (5) visibility
//      (0 = above horizon, 1 = no event, 2 = below horizon)
//

var month = new Array("Jan","Feb","Mar","Apr","May","Jun","Jul",
                      "Aug","Sep","Oct","Nov","Dec");

var p1 = new Array();
var u1 = new Array();
var u2 = new Array();
var mid = new Array();
var u3 = new Array();
var u4 = new Array();
var p4 = new Array();


var currenttimeperiod = "";
var loadedtimeperiods = new Array();

//
// Populate the circumstances array
// entry condition - circumstances[1] must contain the correct value
function populatecircumstances(elements, circumstances) {
  var index, t, ra, dec, h;

  index = obsvconst[4]
  t = circumstances[1]
  ra = elements[18+index] * t + elements[17+index]
  ra = ra * t + elements[16+index]
  dec = elements[21+index] * t + elements[20+index]
  dec = dec * t + elements[19+index]
  dec = dec * Math.PI / 180.0
  circumstances[3] = dec
  h = 15.0*(elements[6+index] + (t - elements[2+index]/3600.0)*1.00273791) - ra
  h = h * Math.PI / 180.0 - obsvconst[1]
  circumstances[2] = h
  circumstances[4] = Math.asin(Math.sin(obsvconst[0]) * Math.sin(dec) + Math.cos(obsvconst[0]) * Math.cos(dec) * Math.cos(h))
  circumstances[4] -= Math.asin(Math.sin(elements[7+index]*Math.PI/180.0) * Math.cos(circumstances[4]))
  if (circumstances[4] * 180.0 / Math.PI < elements[8+index] - 0.5667) {
    circumstances[5] = 2
  } else if (circumstances[4] < 0.0) {
    circumstances[4] = 0.0
    circumstances[5] = 0
  } else {
    circumstances[5] = 0
  }
}

//
// Populate the p1, u1, u2, mid, u3, u4 and p4 arrays
function getall(elements) {
  var pattern, index

  index = obsvconst[4]
  p1[1] = elements[index+9]
  populatecircumstances(elements,p1)
  mid[1] = elements[index+12]
  populatecircumstances(elements,mid)
  p4[1] = elements[index+15]
  populatecircumstances(elements,p4)
  if (elements[index+5] < 3) {
    u1[1] = elements[index+10]
    populatecircumstances(elements,u1)
    u4[1] = elements[index+14]
    populatecircumstances(elements,u4)
    if (elements[index+5] < 2) {
      u2[1] = elements[index+11]
      u3[1] = elements[index+13]
      populatecircumstances(elements,u2)
      populatecircumstances(elements,u3)
    } else {
      u2[5] = 1
      u3[5] = 1
    }
  } else {
    u1[5] = 1
    u2[5] = 1
    u3[5] = 1
    u4[5] = 1
  }
  if ((p1[5] != 0) && (u1[5] != 0) && (u2[5] != 0) && (mid[5] != 0) && (u3[5] != 0) && (u4[5] != 0) && (p4[5] != 0)) {
    mid[5] = 1
  }
}

//
// Read the data that's in the form, and populate the obsvconst array
function readform() {
  var tmp

  // Make sure that we have something to parse from the form
  if (document.eclipseform.latd.value == "") document.eclipseform.latd.value="0"
  if (document.eclipseform.latm.value == "") document.eclipseform.latm.value="0"
  if (document.eclipseform.lats.value == "") document.eclipseform.lats.value="0"
  if (document.eclipseform.lond.value == "") document.eclipseform.lond.value="0"
  if (document.eclipseform.lonm.value == "") document.eclipseform.lonm.value="0"
  if (document.eclipseform.lons.value == "") document.eclipseform.lons.value="0"
  if (document.eclipseform.alt.value == "") document.eclipseform.alt.value="0"

  // Write back to the form what we are parsing
  document.eclipseform.latd.value=Math.abs(parseFloat(document.eclipseform.latd.value))
  document.eclipseform.latm.value=Math.abs(parseFloat(document.eclipseform.latm.value))
  document.eclipseform.lats.value=Math.abs(parseFloat(document.eclipseform.lats.value))
  document.eclipseform.lond.value=Math.abs(parseFloat(document.eclipseform.lond.value))
  document.eclipseform.lonm.value=Math.abs(parseFloat(document.eclipseform.lonm.value))
  document.eclipseform.lons.value=Math.abs(parseFloat(document.eclipseform.lons.value))
  document.eclipseform.alt.value=Math.abs(parseFloat(document.eclipseform.alt.value))

  // Get the latitude
  obsvconst[0]=parseFloat(document.eclipseform.latd.value)+parseFloat(document.eclipseform.latm.value)/60.0+parseFloat(document.eclipseform.lats.value)/3600.0
  obsvconst[0]=obsvconst[0]*parseFloat(document.eclipseform.latx.options[document.eclipseform.latx.selectedIndex].value)
  obsvconst[0]=obsvconst[0]*Math.PI/180.0

  // Get the longitude
  obsvconst[1]=parseFloat(document.eclipseform.lond.value)+parseFloat(document.eclipseform.lonm.value)/60.0+parseFloat(document.eclipseform.lons.value)/3600.0
  obsvconst[1]=obsvconst[1]*parseFloat(document.eclipseform.lonx.options[document.eclipseform.lonx.selectedIndex].value)
  obsvconst[1]=obsvconst[1]*Math.PI/180.0

  // Get the altitude
  obsvconst[2]=parseFloat(document.eclipseform.alt.value)

  // Get the time zone
  obsvconst[3]=parseFloat(document.eclipseform.tzm.options[document.eclipseform.tzm.selectedIndex].value)
  obsvconst[3]=parseFloat(document.eclipseform.tzh.options[document.eclipseform.tzh.selectedIndex].value) + obsvconst[3]/60.0
  obsvconst[3]=parseFloat(document.eclipseform.tzx.options[document.eclipseform.tzx.selectedIndex].value) * obsvconst[3]

  obsvconst[4] = 0
  for (tmp = 0 ; tmp < 3 ; tmp++) {
    if (document.eclipseform.ecltype[tmp].checked) {
      obsvconst[5] = document.eclipseform.ecltype[tmp].value
    }
  }

}

//
// Get the local date of an event
function getdate(elements,circumstances) {
  var t, ans, jd, a, b, c, d, e, index

  index = obsvconst[4]
  // Calculate the JD for noon (TDT) the day before the day that contains T0
  jd = Math.floor(elements[index] - (elements[1+index]/24.0))
  // Calculate the local time (ie the offset in hours since midnight TDT on the day containing T0).
  t = circumstances[1] + elements[1+index] - obsvconst[3] - (elements[2+index] - 30.0) / 3600.0
  if (t < 0.0) {
    jd--;
  }
  if (t >= 24.0) {
    jd++;
  }
  if (jd >= 2299160.0) {
    a = Math.floor((jd - 1867216.25) / 36524.25)
    a = jd + 1 + a - Math.floor(a/4);
  } else {
    a = jd;
  }
  b = a + 1525.0
  c = Math.floor((b-122.1)/365.25)
  d = Math.floor(365.25*c)
  e = Math.floor((b - d) / 30.6001)
  d = b - d - Math.floor(30.6001*e)
  if (e < 13.5) {
    e = e - 1
  } else {
    e = e - 13
  }
  if (e > 2.5) {
    ans = c - 4716 + "-"
  } else {
    ans = c - 4715 + "-"
  }
  ans += month[e-1] + "-"
  if (d < 10) {
    ans = ans + "0"
  }
  ans = ans + d
  return ans
}

//
// Get the local time of an event
function gettime(elements,circumstances) {
  var t, ans, index, html, ital

  ans = ""
  index = obsvconst[4]
  t = circumstances[1] + elements[1+index] - obsvconst[3] - (elements[2+index] - 30.0) / 3600.0
  if (t < 0.0) {
    t = t + 24.0
  }
  if (t >= 24.0) {
    t = t - 24.0
  }
  if (t < 10.0) {
    ans = ans + "0"
  }
  ans = ans + Math.floor(t) + ":"
  t = (t * 60.0) - 60.0 * Math.floor(t)
  if (t < 10.0) {
    ans = ans + "0"
  }
  ans = ans + Math.floor(t)
  if (circumstances[5] == 2) {
    html = document.createElement("font");
    html.setAttribute("color","#808080");
    ital = document.createElement("i");
    ital.appendChild(document.createTextNode(ans));
    html.appendChild(ital);
    return html;
  } else {
    return document.createTextNode(ans);
  }
}

//
// Get the altitude
function getalt(circumstances) {
  var t, ans, html, ital

  t = circumstances[4] * 180.0 / Math.PI
  t = Math.floor(t+0.5)
  if (t < 0.0) {
    ans = "-"
    t = -t
  } else {
    ans = "+"
  }
  if (t < 10.0) {
    ans = ans + "0"
  }
  ans = ans + t
  if (circumstances[5] == 2) {
    html = document.createElement("font");
    html.setAttribute("color","#808080");
    ital = document.createElement("i");
    ital.appendChild(document.createTextNode(ans));
    html.appendChild(ital);
    return html;
  } else {
    return document.createTextNode(ans);
  }
}


function clearoldresults() {
  results = document.getElementById("el_results");
  resultsTable = document.getElementById("el_locationtable");
  if (resultsTable != null) results.removeChild(resultsTable);
  resultsTable = document.getElementById("el_resultstable");
  if (resultsTable != null) results.removeChild(resultsTable);
}

// CALCULATE!
function calculatefor(el) {
  readform()
  clearoldresults();
  results = document.getElementById("el_results");
  p = document.createElement("p");
  p.setAttribute("id","el_locationtable");
  b = document.createElement("h2");
  b.setAttribute("align","center");
  b.appendChild(document.createTextNode("Lunar Eclipses from "+el[0]));
  p.appendChild(b);
  b = document.createElement("h2");
  b.setAttribute("align","center");
  b.appendChild(document.createTextNode(document.eclipseform.loc_name.value));
  p.appendChild(b);
  resultsTable = document.createElement("table");
  resultsTable.setAttribute("border","0");
  tbody = document.createElement("tbody");
  row = document.createElement("tr");
  td = document.createElement("td");
  td.setAttribute("align","right");
  td.setAttribute("nowrap","");
  td.appendChild(document.createTextNode("Latitude: "));
  row.appendChild(td);
  td = document.createElement("td");
  td.setAttribute("nowrap","");
  text = document.eclipseform.latd.value;
  text += "\u00b0 ";
  if (document.eclipseform.latm.value < 10) text += "0";
  text += document.eclipseform.latm.value;
  text += "' ";
  if (document.eclipseform.lats.value < 10) text += "0";
  text += document.eclipseform.lats.value;
  text += '" ';
  text += (document.eclipseform.latx.options[document.eclipseform.latx.selectedIndex]).text;
  td.appendChild(document.createTextNode(text));
  row.appendChild(td);
  tbody.appendChild(row);
  row = document.createElement("tr");
  td = document.createElement("td");
  td.setAttribute("align","right");
  td.setAttribute("nowrap","");
  td.appendChild(document.createTextNode("Longitude: "));
  row.appendChild(td);
  td = document.createElement("td");
  td.setAttribute("nowrap","");
  text = document.eclipseform.lond.value;
  text += "\u00b0 ";
  if (document.eclipseform.lonm.value < 10) text += "0";
  text += document.eclipseform.lonm.value;
  text += "' ";
  if (document.eclipseform.lons.value < 10) text += "0";
  text += document.eclipseform.lons.value;
  text += '" ';
  text += (document.eclipseform.lonx.options[document.eclipseform.lonx.selectedIndex]).text;
  td.appendChild(document.createTextNode(text));
  row.appendChild(td);
  tbody.appendChild(row);
  row = document.createElement("tr");
  td = document.createElement("td");
  td.setAttribute("align","right");
  td.setAttribute("nowrap","");
  td.appendChild(document.createTextNode("Altitude: "));
  row.appendChild(td);
  td = document.createElement("td");
  td.setAttribute("nowrap","");
  text = document.eclipseform.alt.value;
  text += "m";
  td.appendChild(document.createTextNode(text));
  row.appendChild(td);
  tbody.appendChild(row);
  row = document.createElement("tr");
  td = document.createElement("td");
  td.setAttribute("align","right");
  td.setAttribute("nowrap","");
  td.appendChild(document.createTextNode("Time Zone: "));
  row.appendChild(td);
  td = document.createElement("td");
  td.setAttribute("nowrap","");
  text = (document.eclipseform.tzh.options[document.eclipseform.tzh.selectedIndex]).text;
  text += ":";
  text += (document.eclipseform.tzm.options[document.eclipseform.tzm.selectedIndex]).text;
  text += " ";
  text += (document.eclipseform.tzx.options[document.eclipseform.tzx.selectedIndex]).text;
  td.appendChild(document.createTextNode(text));
  row.appendChild(td);
  tbody.appendChild(row);
  resultsTable.appendChild(tbody);
  p.appendChild(resultsTable);
  results.appendChild(p);

  resultsTable = document.createElement("table");
  resultsTable.setAttribute("id","el_resultstable");
  resultsTable.setAttribute("width","150");
  resultsTable.setAttribute("border","2");
  tbody = document.createElement("tbody");
  row = document.createElement("tr");
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Calendar Date"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Ecl. Type"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Pen. Mag."));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Umbral Mag."));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Pen. Eclipse Begins"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Alt"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Partial Eclipse Begins"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Alt"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Total Eclipse Begins"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Alt"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Mid. Eclipse"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Alt"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Total Eclipse Ends"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Alt"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Partial Eclipse Ends"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Alt"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Pen. Eclipse Ends"));
  row.appendChild(td);
  td = document.createElement("th");
  td.appendChild(document.createTextNode("Alt"));
  row.appendChild(td);
  tbody.appendChild(row);
  for (i = 1 ; i < el.length ; i+=22) {
   if (el[5+i] <= obsvconst[5]) {
    obsvconst[4]=i;
    getall(el)
    // Is there an event...
    if (mid[5] != 1) {
      row = document.createElement("tr");
      // Calendar Date
      td = document.createElement("td");
      td.setAttribute("nowrap","")
      val = document.createTextNode(getdate(el,p1));
      td.appendChild(val);
      row.appendChild(td);
      // Eclipse Type
      td = document.createElement("td");
      td.setAttribute("align","center")
      if (el[5+i] == 1) {
        td.appendChild(document.createTextNode("T"))
      } else if (el[5+i] == 2) {
        td.appendChild(document.createTextNode("P"))
      } else {
        td.appendChild(document.createTextNode("N"))
      }
      row.appendChild(td);
      // Pen. Mag
      td = document.createElement("td");
      td.setAttribute("align","right");
      td.appendChild(document.createTextNode(el[3+i]));
      row.appendChild(td);
      // Umbral Mag
      td = document.createElement("td");
      td.setAttribute("align","right");
      td.appendChild(document.createTextNode(el[4+i]));
      row.appendChild(td);
      // P1
      td = document.createElement("td");
      td.setAttribute("align","center")
      td.appendChild(gettime(el, p1));
      row.appendChild(td)
      // P1 alt
      td = document.createElement("td");
      td.setAttribute("align","center")
      td.appendChild(getalt(p1));
      row.appendChild(td)
      if (u1[5] == 1) {
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(document.createTextNode("-"))
        row.appendChild(td);
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(document.createTextNode("-"))
        row.appendChild(td);
      } else {
        // U1
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(gettime(el, u1));
        row.appendChild(td)
        // U1 alt
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(getalt(u1));
        row.appendChild(td)
      }
      if (u2[5] == 1) {
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(document.createTextNode("-"))
        row.appendChild(td);
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(document.createTextNode("-"))
        row.appendChild(td);
      } else {
        // U2
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(gettime(el, u2));
        row.appendChild(td)
        // U2 alt
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(getalt(u2));
        row.appendChild(td)
      }
      // mid
      td = document.createElement("td");
      td.setAttribute("align","center")
      td.appendChild(gettime(el, mid));
      row.appendChild(td)
      // mid alt
      td = document.createElement("td");
      td.setAttribute("align","center")
      td.appendChild(getalt(mid));
      row.appendChild(td)
      if (u3[5] == 1) {
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(document.createTextNode("-"))
        row.appendChild(td);
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(document.createTextNode("-"))
        row.appendChild(td);
      } else {
        // u3
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(gettime(el, u3));
        row.appendChild(td)
        // u3 alt
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(getalt(u3));
        row.appendChild(td)
      }
      if (u4[5] == 1) {
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(document.createTextNode("-"))
        row.appendChild(td);
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(document.createTextNode("-"))
        row.appendChild(td);
      } else {
        // u4
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(gettime(el, u4));
        row.appendChild(td)
        // u4 alt
        td = document.createElement("td");
        td.setAttribute("align","center")
        td.appendChild(getalt(u4));
        row.appendChild(td)
      }
      // P4
      td = document.createElement("td");
      td.setAttribute("align","center")
      td.appendChild(gettime(el, p4));
      row.appendChild(td)
      // P4 alt
      td = document.createElement("td");
      td.setAttribute("align","center")
      td.appendChild(getalt(p4));
      row.appendChild(td)
      tbody.appendChild(row);
    }
   }
  }
  resultsTable.appendChild(tbody);
  results.appendChild(resultsTable);
}

function init() {
  opt = document.getElementById("el_cities");
  for (i = 0 ; i < cities.length ; i+=9) {
    name = String(cities[i]);
    if (name.indexOf("--",0) == 0) {
      group = document.createElement("optgroup");
      group.setAttribute("label",name.substring(2));
      opt.appendChild(group);
      i++;
    }
    city = document.createElement("option");
    city.setAttribute("value",i);
    cityName = document.createTextNode(cities[i]);
    city.appendChild(cityName);
    opt.appendChild(city);
  }
}

function citychange() {
  clearoldresults();
  index = Number(document.eclipseform.cityndx.value);
  if (index <= 0) return;
  hemisphere=0;
  document.eclipseform.loc_name.value = cities[index++];
  val = cities[index++];
  if (val < 0) { val=-val; hemisphere=1; }
  document.eclipseform.latd.value = val;
  val = cities[index++];
  if (val < 0) { val=-val; hemisphere=1; }
  document.eclipseform.latm.value = val;
  val = cities[index++];
  if (val < 0) { val=-val; hemisphere=1; }
  document.eclipseform.lats.value = val;
  document.eclipseform.latx.selectedIndex = hemisphere;
  hemisphere=0;
  val = cities[index++];
  if (val < 0) { val=-val; hemisphere=1; }
  document.eclipseform.lond.value = val;
  val = cities[index++];
  if (val < 0) { val=-val; hemisphere=1; }
  document.eclipseform.lonm.value = val;
  val = cities[index++];
  if (val < 0) { val=-val; hemisphere=1; }
  document.eclipseform.lons.value = val;
  document.eclipseform.lonx.selectedIndex = hemisphere;
  document.eclipseform.alt.value=cities[index++];
  val = cities[index];
  if (val < 0) {
    document.eclipseform.tzx.selectedIndex=1;
    val = -val;
  } else {
    document.eclipseform.tzx.selectedIndex=0;
  }
  document.eclipseform.tzh.selectedIndex = Math.floor(val);
  document.eclipseform.tzm.selectedIndex = Math.floor(4*(val-document.eclipseform.tzh.selectedIndex)+0.5);
}

function newloc() {
  document.eclipseform.cityndx.selectedIndex=0;
  clearoldresults();
}

function settimeperiod(timeperiod) {
  for (i = 0 ; i < loadedtimeperiods.length ; i++) {
    if (loadedtimeperiods[i] == timeperiod) {
      if (eval("self."+timeperiod)) {
        currenttimeperiod = timeperiod;
        eval(timeperiod+"()");
      }
      return;
    }
  }
  currenttimeperiod = timeperiod;
  loadedtimeperiods.push(timeperiod);
  head = document.getElementsByTagName("head")[0];
  script = document.createElement("script");
  script.setAttribute("language","JavaScript");
  script.setAttribute("src",timeperiod+".js");
  script.type = "text/javascript";
  script.defer = false;
  head.appendChild(script);
}

function recalculate() {
  eval(currenttimeperiod+"()");
}

