c = {};
c.CAM_FOV  = 45;
c.CAM_NEAR = 0.1;
c.CAM_FAR  = 200;
c.FOG_NEAR = 10;
c.FOG_FAR  = 200;

g = {};
g.width, g.height;
g.container, g.renderer, g.scene, g.camera, g.controls;
g.stats, g.gui;

g.lightC = [];
g.lightP = [];

g.time = 2.0;

function init() {
  // container
  g.container = document.getElementById("container");
  g.width  = window.innerWidth;
  g.height = window.innerHeight;

  // renderer
  g.renderer = new THREE.WebGLRenderer({ 
    clearAlpha: 0,
    clearColor: 0xAAAAAA,
    antialias: true
  });
  g.renderer.setSize( g.width, g.height );
  g.renderer.autoClear = false;  
  g.container.appendChild( g.renderer.domElement );

  // camera
  g.camera = new THREE.PerspectiveCamera(
    c.CAM_FOV, 
    g.width/g.height,
    c.CAM_NEAR,
    c.CAM_FAR
  );
  g.camera.position.set(0, 0, -2);
  g.camera.lookAt(new THREE.Vector3());

  // scene
  g.scene = new THREE.Scene();
  g.scene.add(g.camera);

  // trackball controls
  g.controls = new THREE.TrackballControls(g.camera, g.container);
  g.controls.rotateSpeed = 1.0;
  g.controls.zoomSpeed = 1.2;
  g.controls.panSpeed = 1.0;    
  g.controls.dynamicDampingFactor = 0.3;
  g.controls.staticMoving = false;
  g.controls.noZoom = false;
  g.controls.noPan = false;

  initScene();

  
  // insert stats
  g.stats = new Stats();
  g.stats.domElement.style.position = 'absolute';
  g.stats.domElement.style.top = '0px';
  g.stats.domElement.style.zIndex = 100;
  g.container.appendChild( g.stats.domElement );
  
  
  // init gui
  g.gui = new dat.GUI({ autoPlace:false });
  $("#gui-container").append(g.gui.domElement);
  
  // hack to edit gui
  $(g.gui.__closeButton).hide();
  $(g.gui.__resize_handle).hide();
  
  // add line
  g.guiline = g.gui.add(g.uniforms.uR, "value").min(0.0).max(255.0).step(1);
  g.guiline.name("R");
  g.guiline = g.gui.add(g.uniforms.uG, "value").min(0.0).max(255.0).step(1);
  g.guiline.name("G");
  g.guiline = g.gui.add(g.uniforms.uB, "value").min(0.0).max(255.0).step(1);
  g.guiline.name("B");
  g.guiline = g.gui.add(g.uniforms.uTMK, "value").min(0.0).max(128.0).step(1);
  g.guiline.name("transmittance ");
  g.guiline = g.gui.add(g.uniforms.uTMK2, "value").min(0.0).max(128.0).step(1);
  g.guiline.name("transmittance 2");
  g.guiline = g.gui.add(g.uniforms.uShininess, "value").min(0.0).max(16.0).step(0.1);
  g.guiline.name("shininess");
  g.guiline = g.gui.add(g.uniforms.uCrust, "value").min(1.0).max(16.0).step(1);
  g.guiline.name("crust influence");
  g.guiline = g.gui.add(g.uniforms.uShin2, "value").min(1.0).max(18.0).step(0.01);
  g.guiline.name("second shininess");
  g.guiline = g.gui.add(g.uniforms.uPhi, "value").min(0.0).max(3.14).step(0.01);
  g.guiline.name("phi");

  window.addEventListener( 'resize', onWindowResize, false );
}

function update() {
  animate();
  g.stats.update();
  g.controls.update();

  // render
  g.renderer.clear();
  g.renderer.render( g.scene, g.camera );

  requestAnimationFrame(update);
};

function onWindowResize(event) {
  g.width  = window.innerWidth;
  g.height = window.innerHeight;

  g.renderer.setSize( g.width, g.height );

  g.camera.aspect = g.width / g.height;
  g.camera.updateProjectionMatrix();

  g.controls.screen.width = g.width;
  g.controls.screen.height = g.height;
  g.controls.radius = ( g.width + g.height ) / 4;
};

function animate() {
  //g.cube.rotation.x += 0.01;
  //g.cube.rotation.y += 0.01;  
  //g.cube.position.y = 2.0*Math.sin(g.time);
  
  g.lightP[0].x = 2.0*Math.sin(g.time);
  g.lightP[0].z = 2.0*Math.cos(g.time);
  g.lightP[0].y = 1.5;
  
  g.lightP[1].x = 2.0;
  g.lightP[1].z = 2.0;
  g.lightP[1].y = 2.0*Math.sin(g.time);
  
  g.time += 0.0055;
}

// inputs THREE.Vector3
function addLight(pos, col) {  
  var light;
  light = new THREE.PointLight();
  light.position.set( pos.x, pos.y, pos.z );
  light.color.setRGB( col.x, col.y, col.z );
  g.scene.add( light );
  
  // add geometry
  var mat = new THREE.MeshBasicMaterial();
  mat.color = light.color;
  var shape = new THREE.Mesh(
    new THREE.SphereGeometry( 0.1, 8, 8 ),
    mat
  );
  shape.position = light.position;
  g.scene.add(shape);
  
  g.lightP.push(light.position);
  g.lightC.push(col);
}

function initScene() {
  
  // fog
  //g.scene.fog = new THREE.Fog( 0x000000, c.FOG_NEAR, c.FOG_FAR );

  //// ground
  //(function() {
  //  var imageCanvas = document.createElement( "canvas" );
  //  var context = imageCanvas.getContext( "2d" );
  //
  //  imageCanvas.width = imageCanvas.height = 128;
  //
  //  context.fillStyle = "#CCC";
  //  context.fillRect( 0, 0, 128, 128 );
  //
  //  context.fillStyle = "#fff";
  //  context.fillRect( 0, 0, 64, 64);
  //  context.fillRect( 64, 64, 64, 64 );
  //
  //  var textureCanvas = new THREE.Texture( imageCanvas, 
  //    THREE.UVMapping, THREE.RepeatWrapping, THREE.RepeatWrapping );
  //  var materialCanvas = new THREE.MeshBasicMaterial( { map: textureCanvas } );
  //
  //  textureCanvas.needsUpdate = true;
  //  textureCanvas.repeat.set( 1000, 1000 );
  //
  //  var geometry = new THREE.PlaneGeometry( 100, 100 );
  //
  //  var meshCanvas = new THREE.Mesh( geometry, materialCanvas );
  //  meshCanvas.scale.set( 100, 100, 100 );
  //  meshCanvas.position.set(0, -1, 0);
  //
  //  g.scene.add(meshCanvas);
  //})();
  
  // lights
  addLight(new THREE.Vector3(2,2,-2), new THREE.Vector3(255/255.0, 255/255.0, 255/255.0));
  addLight(new THREE.Vector3(-2, 1, -3), new THREE.Vector3(253/255.0, 245/255.0, 206/255.0));
 // add subtle ambient lighting
    var ambientLight = new THREE.AmbientLight(0x000000);
    g.scene.add(ambientLight);
  // the cube
  
  var voltex = THREE.ImageUtils.loadTexture("textures/imagenSystem2.png");
  voltex.minFilter = voltex.magFilter = THREE.LinearFilter;
  voltex.wrapS = voltex.wrapT = THREE.ClampToEdgeWrapping;
  var SIDESIZE = 128;
  var voltexDim = new THREE.Vector3(SIDESIZE, SIDESIZE, SIDESIZE);
  
  //var volcol = new THREE.Vector3(189/255.0, 175/255.0, 146/255.0);
  //var volcol = new THREE.Vector3(219/255.0, 204/255.0, 173/255.0);
  var volcol = new THREE.Vector3(252/255.0, 237/255.0, 208/255.0);
  //var volcol = new THREE.Vector3(211/255.0, 209/255.0, 186/255.0);
  //var volcol = new THREE.Vector3(236/255.0, 216/255.0, 179/255.0);
  
  g.offset = new THREE.Vector3();
    
  g.uniforms = {
    uCamPos:    { type: "v3", value: g.camera.position },
    uLightP:    { type: "v3v", value: g.lightP },
    uLightC:    { type: "v3v", value: g.lightC },
    uColor:     { type: "v3", value: volcol },
    uTex:       { type: "t", value: 0, texture: voltex },
    uTexDim:    { type: "v3", value: voltexDim },
    uOffset:    { type: "v3", value: g.offset },
    uTMK:       { type: "f", value: 4.0 },
    uTMK2:      { type: "f", value: 25.0 },
    uShininess: { type: "f", value: 1.0 },
    uCrust:     { type: "f", value: 4.0 },
    uShin2:     { type: "f", value: 2.8 },
    uR:         { type: "f", value: 152.0 },
    uG:         { type: "f", value: 137.0 },
    uB:         { type: "f", value: 108.0 },
    uPhi:         { type: "f", value: 1.0 },
  }
  
  var shader = new THREE.ShaderMaterial({
    uniforms:       g.uniforms,
    vertexShader:   loadTextFile("shaders/vol-vs.glsl"),
    fragmentShader: loadTextFile("shaders/vol-fs.glsl")
  });

  var shader2 = new THREE.ShaderMaterial({
    uniforms:       g.uniforms,
    vertexShader:   loadTextFile("shaders/vol-vs.glsl"),
    fragmentShader: loadTextFile("shaders/vol-fs2.glsl")
  });
  
  // debug with wireframe
  //g.cube = THREE.SceneUtils.createMultiMaterialObject(
  //  new THREE.CubeGeometry( 1.0, 1.0, 1.0 ),
  //  [
  //    shader,
  //    new THREE.MeshBasicMaterial( { wireframe: true, transparent: true, opacity: 0.1 } )
  //  ]
  //)
    var texture, material, plane;

    texture = THREE.ImageUtils.loadTexture( "textures/wood.jpg" );
    texture.wrapT = THREE.RepeatWrapping;  // This doesn't seem to work;
    material = new THREE.MeshLambertMaterial({ map : texture });
    plane = new THREE.Mesh(new THREE.PlaneGeometry(5, 5), material);
    plane.doubleSided = true;
    plane.position.y = -0.55;
    //plane.rotation.z = 0;  // Not sure what this number represents.
    //g.scene.add(plane);

  g.cube = new THREE.Mesh(
    new THREE.CubeGeometry( 1.0, 1.0, 1.0 ),    // must be unit cube
    shader //new THREE.MeshLambertMaterial( { color: 0xCCCCCC } )
  );
  g.cube2 = new THREE.Mesh(
    new THREE.CubeGeometry( 1.0, 1.0, 1.0 ),    // must be unit cube
    shader2 //new THREE.MeshLambertMaterial( { color: 0xCCCCCC } )
  );

  //g.cube2.position.set(2.0, 0.0, 0.0);
  //g.cube2.scale.set(1.1, 1.1, 1.1);      // scale later
  //g.cube2.rotation.set(0.0, 0.0, 0.0);      // scale later
  //g.cylinder.positon.set(0.0, 0.0, 0.0);
  //g.cube.position.set(0.0, 0.0, 0.0);
  //g.scene.add(g.cube);
  g.cube2.position.set(0.0, 0.0, 0.0);
  g.scene.add(g.cube2);
  //g.scene.add(g.cylinder);

}

// perform synchronous ajax load
function loadTextFile(url) {
  var result;
  
  $.ajax({
    url:      url,
    type:     "GET",
    async:    false,
    dataType: "text",
    success:  function(data) {
      result = data;
    }
  });
  
  return result;
}

function mousetrap() {
  var STEP = 0.05;
  
  Mousetrap.bind("up", function() {
    g.offset.z-=STEP;
  });
  Mousetrap.bind("down", function() {
    g.offset.z+=STEP;
  });
  Mousetrap.bind("left", function() {
    g.offset.y-=STEP;
  });
  Mousetrap.bind("right", function() {
    g.offset.y+=STEP;
  });
  
  Mousetrap.bind("shift+r", function() {
    console.log("hotkey: reset camera");
    g.camera.position.set(2, 2, -2);
    g.camera.up.set(0, 1, 0);
    g.camera.lookAt(new THREE.Vector3(0,0,0));
  });
}

$(function() {
  init();
  update();
  mousetrap();
});
