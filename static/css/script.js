function openForm() {
    document.getElementById("myForm").style.display = "block";
}
function closeForm() {
  document.getElementById("myForm").style.display = "none";
}
function openEvForm() {
  document.getElementById("myEvForm").style.display = "block";
}
function closeEvForm() {
  document.getElementById("myEvForm").style.display = "none";
}

// all the code below is only for the movement pop up
const addBtn = document.querySelector(".add");
const input = document.querySelector(".input_group");

function removeInput() {
  this.parentElement.parentElement.remove()
}

function addInput() {
  console.log('this working??')
  mvmt_type = document.createElement('select');
  for (let i = 0; i < site_info[4].length; i++){
    var val = new Option(site_info[4][i][1], site_info[4][i][0]);
    mvmt_type.appendChild(val);
  }
  mvmt_type.name = "mvmt_type"

  const callsign = document.createElement("input");
  callsign.type = "text";
  callsign.placeholder = "Enter Movement Name";
  callsign.name = "cs";

  const origin = document.createElement("input");
  origin.type = "text";
  origin.placeholder = "Enter Origin";
  origin.name = "ol";

  const dest = document.createElement("input");
  dest.type = "text";
  dest.placeholder = "Enter Destination";
  dest.name = "dn"

  const start_date = document.createElement("input");
  start_date.setAttribute("type", "date");
  start_date.name = "sd"

  const start_time = document.createElement("input");
  start_time.setAttribute("type", "time");
  start_time.name = "start_t"

  const end_date = document.createElement("input");
  end_date.setAttribute("type", "date");
  end_date.name = "ed"

  const end_time = document.createElement("input");
  end_time.setAttribute("type", "time");
  end_time.name = "end_t"

  const btn = document.createElement("a");
  btn.className = "delete";
  btn.innerHTML = "&times";

  btn.addEventListener("click", removeInput);

  const contain = document.createElement("div");
  contain.className = "contain";

  const info_contatin = document.createElement("div");
  info_contatin.className = "info_contain";

  // select div
  const select_div = document.createElement("div");
  select_div.className = "inside_div";
  // callsign div
  const call_div = document.createElement("div");
  call_div.className = "inside_div";
  // origin div
  const origin_div = document.createElement("div");
  origin_div.className = "inside_div";
  // destination div
  const dest_div = document.createElement("div");
  dest_div.className = "inside_div";
  //start time div
  const start_div = document.createElement("div");
  start_div.className = "inside_div";
  // end time div
  const end_div = document.createElement("div");
  end_div.className = "inside_div";

  const close_but_div = document.createElement("div");
  close_but_div.className = "close_but_div";

  const mvmt_label = document.createElement("p");
  mvmt_label.textContent = "Select Movement Type";

  const cs_label = document.createElement("p");
  cs_label.textContent = "Enter Movement Name";

  const origin_label = document.createElement("p");
  origin_label.textContent = "Enter Origin";

  const dest_label = document.createElement("p");
  dest_label.textContent = "Enter Destination";

  const start_label = document.createElement("p");
  start_label.textContent = "Choose Start Date/Time";

  const end_label = document.createElement("p");
  end_label.textContent = "Choose End Date/Time";
  
  input.appendChild(contain);
  contain.appendChild(info_contatin);
  info_contatin.appendChild(select_div);
  info_contatin.appendChild(call_div);
  info_contatin.appendChild(origin_div);
  info_contatin.appendChild(dest_div);
  info_contatin.appendChild(start_div);
  info_contatin.appendChild(end_div);

  contain.appendChild(close_but_div);

  select_div.appendChild(mvmt_label);
  select_div.appendChild(mvmt_type);

  call_div.appendChild(cs_label)
  call_div.appendChild(callsign)

  origin_div.appendChild(origin_label);
  origin_div.appendChild(origin);

  dest_div.appendChild(dest_label);
  dest_div.appendChild(dest);

  start_div.appendChild(start_label);
  start_div.appendChild(start_date);
  start_div.appendChild(start_time)

  end_div.appendChild(end_label)
  end_div.appendChild(end_date);
  end_div.appendChild(end_time);

  close_but_div.appendChild(btn);
}

addBtn.addEventListener("click", addInput);