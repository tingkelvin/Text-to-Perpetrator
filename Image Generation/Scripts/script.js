// const AIRTABLEkey = AIRTABLEkey;
const AIRTABLEkey = "keyk57g7IVGfEc6iZ";
const UNSPLASHkey = "AH7ETnIZeyTWrTkeAjLOM53TFdNgnKirGAzDaQO_Qg4";

var override_output;

("use strict");
var base_model,
  hair_model,
  top_model,
  bottom_model,
  shoe_model,
  accessory_model;
var base_link, hair_link, top_link, bottom_link, shoe_link, accessory_link;
var hair_input,
  top_input,
  bottom_input,
  shoe_input,
  accessory_input,
  race_input,
  base_input;
var hair_color,
  top_color,
  bottom_color,
  shoe_color,
  accessory_color,
  race_color;
var texture_link;
var color_json,
  race_json,
  base_json,
  top_json,
  bottom_json,
  shoe_json,
  accessory_json,
  hair_json;
const renderer = new THREE.WebGLRenderer({
  canvas: document.querySelector("canvas.webgl")
});

const camera = new THREE.PerspectiveCamera(70, 2, 0.5, 1000);
camera.position.z = 1;
camera.position.y = 0;

// Create the link
const light1 = new THREE.PointLight(0xffffff, 0.5, 0);
light1.position.set(200, 100, 300);
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);

// GLTF loader
const gltfLoader = new THREE.GLTFLoader();
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1f1f1f);

// Setup the default Material for all type

//base - Gender - Race
var mode;
var race_material = new THREE.MeshPhysicalMaterial({
  color: 0xffffff
});

//Hair
var hair_material = new THREE.MeshPhysicalMaterial({
  color: 0xffffff
});

//Top
var top_material = new THREE.MeshPhysicalMaterial({
  color: 0xffffff
});

//Bottom
var bottom_material = new THREE.MeshPhysicalMaterial({
  color: 0xffffff
});

//Shoes
var shoe_material = new THREE.MeshPhysicalMaterial({
  color: 0xffffff
});

//Accessories
var accessory_material = new THREE.MeshPhysicalMaterial({
  color: 0xffffff
});

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableZoom = false;
controls.enablePan = false;

base_input = "female";
base_link =
  "https://dl.airtable.com/.attachments/b74d3391cef1e8d44062d6a4a9bf9efe/f8f3612b/female.glb";
init();

function init() {
  addModel(base_model, base_link, race_material);
  scene.add(light1, ambientLight);
  clearSelect();
  clearImg();
  //APPEND EVERY DATABASE RECORD TO SELECT
  getColor();
  getRace();
  getBase();
  getTop();
  getBottom();
  getShoe();
  getAccessory();
}

requestAnimationFrame(animate);

$("#sample").click(async function () {
  const sample_data = await fetch(
    `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Sample?api_key=${AIRTABLEkey}`
  );
  $("#sample").text("Getting Sentence");
  const sample_json = await sample_data.json();
  $("#sample").text("Get Another");
  // if (sample_json.records != undefined) {
  if (sample_json.records.length != 0) {
    var sentence =
      sample_json.records[
        Math.floor(Math.random() * sample_json.records.length)
      ].fields.REALSAMPLE;
    $("#sentence").val(sentence);
  }
  // }
});
var data_json;
$("#generate").click(async function () {
  $("#generate").text("Waiting");
  var sentence = $("#sentence").val();
  var url = `https://mci-75aymfmqxq-ts.a.run.app/predict?text=${sentence}`;
  let response = await fetch(url, {
    method: "GET", // POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json"
    }
  });

  let data = await response.text();
  data_json = JSON.parse(data);
  console.log(data_json);
  $("#output").val(data);
  base_input = data_json.gender;
  race_input = data_json.race;
  top_input = data_json.top;
  bottom_input = data_json.bottom;
  shoe_input = data_json.footwear;
  accessory_input = data_json.accessory;
  hair_style = data_json.hair_style;
  hair_len = data_json.hair_len;
  hair_input = hair_len + ", " + hair_style;

  top_color = data_json.top_color;
  bottom_color = data_json.bottom_color;
  shoe_color = data_json.footwear_color;
  accessory_color = data_json.accessory_color;
  hair_color = data_json.hair_color;
  $("#top-color-text").html(top_color);

  $("#bottom-color-text").html(bottom_color);
  $("#shoe-color-text").html(shoe_color);
  $("#accessory-color-text").html(accessory_color);
  $("#hair-color-text").html(hair_color);
  $("#race-text").html(race_input);
  $("#update").click();
  $(".welcome-banner").hide();
  $("#generate").text("Generate");
});

$("#update").click(function () {
  scene.clear();
  scene.add(light1, ambientLight);
});

$("#update-override").click(function () {
  base_input = $("#gender-2").val();
  race_input = $("#race").val();
  top_input = $("#top").val();
  bottom_input = $("#bottom").val();
  shoe_input = $("#shoe").val();
  accessory_input = $("#accessory").val();

  top_color = $("#top-color").val();
  bottom_color = $("#bottom-color").val();
  shoe_color = $("#shoe-color").val();
  accessory_color = $("#accessory-color").val();
  hair_color = $("#hair-color").val();
  hair_style = $("#hair-style").val();
  hair_len = $("#hair-length").val();
  $("#update").click();
});

$("#update").click(async function () {
  $("#gender-2").val(base_input);
  $("#gender-text").html(base_input);
  $("#race").val(race_input);
  $("#race-text").html(race_input);
  $("#top").val(top_input);
  $("#top-type-text").html(top_input);
  $("#bottom").val(bottom_input);
  $("#bottom-type-text").html(bottom_input);
  $("#shoe").val(shoe_input);
  $("#shoe-type-text").html(shoe_input);
  $("#accessory").val(accessory_input);
  $("#accessory-type-text").html(accessory_input);
  $("#hair-style").val(hair_style);
  $("#hair-style-text").html(hair_style);
  $("#hair-length").val(hair_len);
  $("#hair-length-text").html(hair_len);
  $("#hair-color").val(hair_color);
  $("#hair-color-text").html(hair_color);
  clearImg();
  var top_color_input,
    bottom_color_input,
    hair_color_input,
    accessory_color_input,
    shoe_color_input;
  //Get the images
  top_color_input = top_color + " " + top_input;
  console.log(top_color_input);
  getimage(top_color_input, "top");

  //Bottom
  bottom_color_input = bottom_color + " " + bottom_input;
  console.log(bottom_color_input);
  getimage(bottom_color_input, "bottom");

  hair_color_input = hair_color + " " + hair_len + " " + hair_style + " hair";
  //Hair
  console.log(hair_color_input);
  getimage(hair_color_input, "hair");

  accessory_color_input = accessory_color + " " + accessory_input;
  //Accessory
  console.log(accessory_color_input);
  getimage(accessory_input, "accessory");

  shoe_color_input = shoe_color + " " + shoe_input;
  //Shoes
  console.log(shoe_color_input);
  getimage(shoe_color_input, "shoe");

  //Get Color
  const color_data = await fetch(
    `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Color?api_key=${AIRTABLEkey}`
  );
  const color_json = await color_data.json();

  for (let i = 0; i < color_json.records.length; i++) {
    if (top_color == color_json.records[i].fields.Name) {
      top_material.color.setHex(color_json.records[i].fields.color);
      $("#top-color").val(top_color);
      //$("#top-color-text").html($("#top-color").val());
    }

    if (bottom_color == color_json.records[i].fields.Name) {
      bottom_material.color.setHex(color_json.records[i].fields.color);
      $("#bottom-color").val(bottom_color);

      //$("#bottom-color-text").html($("#bottom-color").val());
    }

    if (shoe_color == color_json.records[i].fields.Name) {
      shoe_material.color.setHex(color_json.records[i].fields.color);
      $("#shoe-color").val(shoe_color);

      //$("#shoe-color-text").html($("#shoe-color").val());
    }

    if (accessory_color == color_json.records[i].fields.Name) {
      accessory_material.color.setHex(color_json.records[i].fields.color);
      $("#accessory-color").val(accessory_color);
      //$("#accessory-color-text").html($("#accessory-color").val());
    }

    if (hair_color == color_json.records[i].fields.Name) {
      hair_material.color.setHex(color_json.records[i].fields.color);
      $("#hair-color").val(hair_color);

      //$("#hair-color-text").html(data_json.hair_color);
    }
  }

  if (race_input == "NA") {
    race_input = 0xffdbac;
  }

  //Get Race Color
  const race_data = await fetch(
    `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Race?api_key=${AIRTABLEkey}&filterByFormula=SEARCH("${race_input}",{Name})`
  );
  const race_json = await race_data.json();
  if (race_json.records.length != 0) {
    race_color = race_json.records[0].fields.color;
    race_material.color.setHex(race_color);
  }

  //base moodel
  const base_data = await fetch(
    `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Gender?api_key=${AIRTABLEkey}&filterByFormula=SEARCH("${base_input}",{Name})`
  );
  const base_json = await base_data.json();
  base_link = base_json.records[0].fields.URL;
  addModel(base_model, base_link, race_material);

  //top
  if (top_input != "NA") {
    const top_data = await fetch(
      `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Top?api_key=${AIRTABLEkey}&filterByFormula=SEARCH("${top_input}",{Name})`
    );
    const top_json = await top_data.json();

    if (top_json.records.length != 0) {
      url_json = top_json.records[0].fields.URL;
      if (url_json.hasOwnProperty("error") == false) {
        if (url_json.includes("https://")) {
          top_link = top_json.records[0].fields.URL;
          addModel(top_model, top_link, top_material);
        } else {
          $("#top").val("N/A");
        }
      }
    }
  }

  //bottom
  if (bottom_input != "NA") {
    const bottom_data = await fetch(
      `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Bottom?api_key=${AIRTABLEkey}&filterByFormula=SEARCH("${bottom_input}",{Name})`
    );
    const bottom_json = await bottom_data.json();

    if (bottom_json.records.length != 0) {
      url_json = bottom_json.records[0].fields.URL;
      if (url_json.hasOwnProperty("error") == false) {
        if (url_json.includes("https://")) {
          bottom_link = bottom_json.records[0].fields.URL;
          addModel(bottom_model, bottom_link, bottom_material);
        } else {
          $("#bottom").val("N/A");
        }
      }
    }
  }

  //shoes
  if (shoe_input != "NA") {
    const shoe_data = await fetch(
      `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Shoes?api_key=${AIRTABLEkey}&filterByFormula=SEARCH("${shoe_input}",{Name})`
    );
    const shoe_json = await shoe_data.json();
    if (shoe_json.records.length != 0) {
      url_json = shoe_json.records[0].fields.URL;
      if (url_json.hasOwnProperty("error") == false) {
        if (url_json.includes("https://")) {
          shoe_link = shoe_json.records[0].fields.URL;
          addModel(shoe_model, shoe_link, shoe_material);
        } else {
          $("#shoe").val("N/A");
        }
      }
    }
  }

  //Accessories
  if (accessory_input != "NA") {
    const accessory_data = await fetch(
      `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Accessory?api_key=${AIRTABLEkey}&filterByFormula=SEARCH("${accessory_input}",{Name})`
    );
    const accessory_json = await accessory_data.json();
    if (accessory_json.records.length != 0) {
      url_json = accessory_json.records[0].fields.URL;
      if (url_json.hasOwnProperty("error") == false) {
        if (url_json.includes("https://")) {
          accessory_link = accessory_json.records[0].fields.URL;
          addModel(accessory_model, accessory_link, accessory_material);
        } else {
          $("#accessory").val("N/A");
        }
      }
    }
  }
  // Hair
  // filterByFormula=(FIND("Plate",{Product Name}))
  const hair_data = await fetch(
    `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Hair?api_key=${AIRTABLEkey}&filterByFormula=AND(AND(SEARCH("${hair_style}",{Hair Style}),SEARCH("${base_input}",{Gender})),SEARCH("${hair_len}",{Hair Length}))`
    //,(SEARCH("${hair_len}",{Hair Length}))
    // %7BName%7D%3D%27${hair_input}%27
  );
  const hair_json = await hair_data.json();
  if (hair_json.records.length != 0) {
    url_json = hair_json.records[0].fields.URL;
    if (url_json.hasOwnProperty("error") == false) {
      if (url_json.includes("https://")) {
        hair_link = hair_json.records[0].fields.URL;
        addModel(hair_model, hair_link, hair_material);
      } else {
        $("#hair").val("N/A");
      }
    }
  }
});

function addModel(model, link, material) {
  gltfLoader.load(link, (base) => {
    model = base.scene;
    model.position.x = 0;
    model.position.z = 0;
    model.position.y = -0.5;
    model.traverse((o) => {
      if (o.isMesh) o.material = material;
      if (o.material) {
        o.material.side = THREE.DoubleSide;
      }
    });
    scene.add(model);
  });
}

function resizeCanvasToDisplaySize() {
  const canvas = renderer.domElement;
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;
  if (canvas.width !== width || canvas.height !== height) {
    // you must pass false here or three.js sadly fights the browser
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  }
}

function animate(time) {
  time *= 0.001; // seconds
  resizeCanvasToDisplaySize();
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}

function clearSelect() {
  //Clear Select
  $("#top-color").empty();
  $("#bottom-color").empty();
  $("#shoe-color").empty();
  $("#accessory-color").empty();
  $("#hair-color").empty();
  $("#race").empty();
  $("#gender-2").empty();
  $("#top").empty();
  $("#bottom").empty();
  $("#shoe").empty();
  $("#accessory").empty();
}

function clearImg() {
  $(`#image_top`).empty();
  $(`#image_bottom`).empty();
  $(`#image_shoe`).empty();
  $(`#image_hair`).empty();
  $(`#image_accessory`).empty();
}

//Get Color
async function getColor() {
  const response = await fetch(
    `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Color?api_key=${AIRTABLEkey}`
  );
  color_json = await response.json(); // Extracting data as a JSON Object from the response;
  // console.log(color_json);
  for (let i = 0; i < color_json.records.length; i++) {
    $("#top-color").append(
      new Option(
        color_json.records[i].fields.Name,
        color_json.records[i].fields.Name
      )
    );
    $("#bottom-color").append(
      new Option(
        color_json.records[i].fields.Name,
        color_json.records[i].fields.Name
      )
    );
    $("#shoe-color").append(
      new Option(
        color_json.records[i].fields.Name,
        color_json.records[i].fields.Name
      )
    );
    $("#accessory-color").append(
      new Option(
        color_json.records[i].fields.Name,
        color_json.records[i].fields.Name
      )
    );
    $("#hair-color").append(
      new Option(
        color_json.records[i].fields.Name,
        color_json.records[i].fields.Name
      )
    );
  }
}

//Get race
async function getRace() {
  const response = await fetch(
    `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Race?api_key=${AIRTABLEkey}`
  );
  race_json = await response.json(); // Extracting data as a JSON Object from the response
  //Get Race Color
  //Assign race name to race select
  for (let i = 0; i < race_json.records.length; i++) {
    $("#race").append(
      new Option(
        race_json.records[i].fields.Name,
        race_json.records[i].fields.Name
      )
    );
  }
}

//Get Base
async function getBase() {
  const response = await fetch(
    `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Gender?api_key=${AIRTABLEkey}`
  );
  base_json = await response.json(); // Extracting data as a JSON Object from the response
  //base moodel
  for (let i = 0; i < base_json.records.length; i++) {
    $("#gender-2").append(
      new Option(
        base_json.records[i].fields.Name,
        base_json.records[i].fields.Name
      )
    );
  }
}

//Get Top
async function getTop() {
  const response = await fetch(
    `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Top?api_key=${AIRTABLEkey}`
  );
  top_json = await response.json(); // Extracting data as a JSON Object from the response
  //top
  for (let i = 0; i < top_json.records.length; i++) {
    $("#top").append(
      new Option(
        top_json.records[i].fields.Name,
        top_json.records[i].fields.Name
      )
    );
  }
}

//Get Bottom
async function getBottom() {
  const response = await fetch(
    `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Bottom?api_key=${AIRTABLEkey}`
  );
  bottom_json = await response.json(); // Extracting data as a JSON Object from the response
  //bottom
  for (let i = 0; i < bottom_json.records.length; i++) {
    $("#bottom").append(
      new Option(
        bottom_json.records[i].fields.Name,
        bottom_json.records[i].fields.Name
      )
    );
  }
}

//Get Shoe
async function getShoe() {
  const response = await fetch(
    `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Shoes?api_key=${AIRTABLEkey}`
  );
  shoe_json = await response.json(); // Extracting data as a JSON Object from the response
  //shoes
  for (let i = 0; i < shoe_json.records.length; i++) {
    $("#shoe").append(
      new Option(
        shoe_json.records[i].fields.Name,
        shoe_json.records[i].fields.Name
      )
    );
  }
}

//Get Accessory
async function getAccessory() {
  const response = await fetch(
    `https://api.airtable.com/v0/appryTwRh1MuFnOyq/Accessory?api_key=${AIRTABLEkey}`
  );
  accessory_json = await response.json(); // Extracting data as a JSON Object from the response
  //Accessory
  for (let i = 0; i < accessory_json.records.length; i++) {
    $("#accessory").append(
      new Option(
        accessory_json.records[i].fields.Name,
        accessory_json.records[i].fields.Name
      )
    );
  }
}

//Get image from input
async function getimage(input, type) {
  switch (type) {
    case "top":
      const top_response = await fetch(
        `https://api.unsplash.com/search/photos?client_id=${UNSPLASHkey}&query=${input}`
      );
      var top_image_json = await top_response.json(); // Extracting data as a JSON Object from the response
      for (let i = 0; i < 4; i++) {
        $(`#image_top`).prepend(
          `<div class="image-search"><a target="_blank" rel="noopener noreferrer" href="${top_image_json.results[i].links.html}"><img class="image" src="${top_image_json.results[i].urls.small}" /></a>`
        );
      }
      break;
    case "bottom":
      const bottom_response = await fetch(
        `https://api.unsplash.com/search/photos?client_id=${UNSPLASHkey}&query=${input}`
      );
      var bottom_image_json = await bottom_response.json();
      for (let i = 0; i < 4; i++) {
        $(`#image_bottom`).prepend(
          `<div class="image-search"><a target="_blank" rel="noopener noreferrer" href="${bottom_image_json.results[i].links.html}"><img class="image" src="${bottom_image_json.results[i].urls.small}" /></a></div>`
        );
      }
      break;
    case "hair":
      const hair_response = await fetch(
        `https://api.unsplash.com/search/photos?client_id=${UNSPLASHkey}&query=${input}`
      );
      var hair_image_json = await hair_response.json();
      for (let i = 0; i < 4; i++) {
        $(`#image_hair`).prepend(
          `<div class="image-search"><a target="_blank" rel="noopener noreferrer" href="${hair_image_json.results[i].links.html}"><img class="image" src="${hair_image_json.results[i].urls.small}" /></a></div>`
        );
      }
      break;
    case "shoe":
      const shoe_response = await fetch(
        `https://api.unsplash.com/search/photos?client_id=${UNSPLASHkey}&query=${input}`
      );
      var shoe_image_json = await shoe_response.json();
      for (let i = 0; i < 4; i++) {
        $(`#image_shoe`).prepend(
          `<div class="image-search"><a target="_blank" rel="noopener noreferrer" href="${shoe_image_json.results[i].links.html}"><img class="image" src="${shoe_image_json.results[i].urls.small}" /></a></div>`
        );
      }
      break;
    case "accessory":
      const accessory_response = await fetch(
        `https://api.unsplash.com/search/photos?client_id=${UNSPLASHkey}&query=${input}`
      );
      var accessory_image_json = await accessory_response.json();
      for (let i = 0; i < 4; i++) {
        $(`#image_accessory`).prepend(
          `<div class="image-search"><a target="_blank" rel="noopener noreferrer" href="${accessory_image_json.results[i].links.html}"><img class="image" src="${accessory_image_json.results[i].urls.small}" /></a></div>`
        );
      }
      break;
  }
}
