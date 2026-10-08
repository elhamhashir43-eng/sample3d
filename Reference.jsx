import React,{Suspense,useEffect,useRef,useState,useMemo,Component} from 'react';
import {createRoot} from 'react-dom/client';
import {Canvas,useFrame,useThree} from '@react-three/fiber';
import {OrbitControls,useGLTF,Environment,Lightformer,Sky} from '@react-three/drei';
import {EffectComposer,Bloom,N8AO} from '@react-three/postprocessing';
import * as THREE from 'three';
import './reference.css';
const TARGET=new THREE.Vector3(0,3.35,0);
const VIEWS={'Front':[0,4.8,27],'Back':[0,5,-27],'Left':[-29,6.5,0],'Right':[29,6.5,0],'Front Left':[-20,10,25],'Front Right':[20,10,25],'Aerial':[17,26,20],'Top / Floor':[0,32,.1]};
function House({night,onReady,roof,floor}){
 const {scene}=useGLTF(`${import.meta.env.BASE_URL}two-storey/house.glb?v=8`);
 useEffect(()=>{scene.traverse(o=>{if(!o.isMesh)return;const m=o.material;const glass=m.name.includes('glass');o.castShadow=!glass&&!m.name.startsWith('Leaf');o.receiveShadow=true;
 if(glass){m.transparent=true;m.depthWrite=false;m.opacity=m.name==='Window glass'?.095:.14;m.envMapIntensity=night?.5:1.1;m.side=THREE.DoubleSide;}
 if(m.name==='Light diffuser')m.emissiveIntensity=night?4:.1;
 if(m.name.startsWith('Leaf'))m.side=THREE.DoubleSide;
 });onReady();},[scene,night,onReady]);
 useEffect(()=>{scene.traverse(o=>{if(!o.isMesh)return;const l=o.userData.level;o.visible=l==='Site'||(l==='Roof'?roof&&floor==='All':floor==='Ground'?(l==='Ground'):floor==='First'?(l==='First'):true);});},[scene,roof,floor]);
 return <primitive object={scene}/>;
}
function Fixture({spec,night}){
 const target=useMemo(()=>{let o=new THREE.Object3D();if(spec.target)o.position.set(...spec.target);return o;},[spec]);
 const lamp=useRef();
 const x=spec.position[0],h=spec.position[1];
 const shadow=!!spec.shadow;
 useEffect(()=>{if(lamp.current&&shadow)lamp.current.shadow.needsUpdate=true;},[night,shadow]);
 const intensity=night?spec.intensity*(spec.kind==='point'?.62:.68):0;
 if(spec.kind==='point')return <pointLight ref={lamp} position={spec.position} color="#ffd2a0" intensity={intensity} distance={7} decay={2} castShadow={shadow} shadow-autoUpdate={false} shadow-mapSize={[512,512]} shadow-bias={-.0005} shadow-normalBias={.03}/>;
 return <><primitive object={target}/><spotLight position={spec.position} target={target} color="#ffd099" intensity={intensity} angle={spec.angle} penumbra={.75} distance={9} decay={2}/></>;
}
function CameraRig({view,reset,onMove}){
 const ref=useRef(),dest=useRef(),{camera,size}=useThree();
 useEffect(()=>{const factor=Math.max(1,1.45/(size.width/size.height));const offset=new THREE.Vector3(...VIEWS[view]).sub(TARGET).multiplyScalar(factor);if(offset.length()>62)offset.setLength(62);dest.current=offset.add(TARGET);},[view,reset,size.width,size.height]);
 useFrame((_,dt)=>{if(!ref.current)return;if(dest.current){const f=1-Math.exp(-dt*4);const current=new THREE.Spherical().setFromVector3(camera.position.clone().sub(ref.current.target));const next=new THREE.Spherical().setFromVector3(dest.current.clone().sub(TARGET));const turn=THREE.MathUtils.euclideanModulo(next.theta-current.theta+Math.PI,Math.PI*2)-Math.PI;current.theta+=turn*f;current.phi=THREE.MathUtils.lerp(current.phi,next.phi,f);current.radius=THREE.MathUtils.lerp(current.radius,next.radius,f);ref.current.target.lerp(TARGET,f);camera.position.copy(ref.current.target).add(new THREE.Vector3().setFromSpherical(current));ref.current.update();if(camera.position.distanceTo(dest.current)<.015)dest.current=null;}
 // Bound pan as well as orbit, maintaining clearance from the building envelope.
 ref.current.target.x=THREE.MathUtils.clamp(ref.current.target.x,-3,3);ref.current.target.y=THREE.MathUtils.clamp(ref.current.target.y,1.6,5.8);ref.current.target.z=THREE.MathUtils.clamp(ref.current.target.z,-3,3);
 if(camera.position.y<.65)camera.position.y=.65;
 });
 return <OrbitControls ref={ref} makeDefault target={TARGET} enableDamping dampingFactor={.085} minDistance={14} maxDistance={65} minPolarAngle={.003} maxPolarAngle={Math.PI/2-.035} zoomSpeed={.65} rotateSpeed={.65} panSpeed={.6} onStart={()=>{dest.current=null;onMove();}}/>;
}
function Scene({night,view,reset,onMove,onReady,lights,roof,floor}){
 const bg=night?'#22354e':'#bdcbd0';
 return <><color attach="background" args={[bg]}/><fog attach="fog" args={[bg,65,160]}/>
 {!night&&<Sky distance={450000} sunPosition={[-30,35,80]} turbidity={3.8} rayleigh={.8} mieCoefficient={.006} mieDirectionalG={.8}/>}
 <hemisphereLight args={[night?'#adc2ed':'#e7f0ff',night?'#414333':'#8a826c',night?.55:1.2]}/>
 <directionalLight position={[12,9,16]} color="#e4eeff" intensity={night?.08:.4}/>
 <directionalLight position={[-13,19,14]} color={night?'#95b4ee':'#fff0d9'} intensity={night?.36:2.7} castShadow shadow-mapSize={[2048,2048]} shadow-camera-left={-20} shadow-camera-right={20} shadow-camera-top={18} shadow-camera-bottom={-18} shadow-camera-far={65} shadow-normalBias={.045} shadow-bias={-.0003}/>
 <Environment resolution={128} frames={1} environmentIntensity={night?.20:.8}><Lightformer intensity={2} color="#e0edff" position={[0,15,0]} rotation={[-Math.PI/2,0,0]} scale={[40,40,1]}/><Lightformer intensity={1.8} color="#fff2dc" position={[-14,7,18]} rotation={[0,-.4,0]} scale={[12,10,1]}/></Environment>
 <Suspense fallback={null}><House {...{night,onReady,roof,floor}}/></Suspense>
 {lights.map((s,i)=><Fixture key={i} spec={s} night={night}/>)}
 <mesh rotation={[-Math.PI/2,0,0]} position={[0,-.39,0]} receiveShadow><planeGeometry args={[250,250]}/><meshStandardMaterial color={night?'#18241c':'#697754'} roughness={1}/></mesh>
 <CameraRig {...{view,reset,onMove}}/>
 <EffectComposer multisampling={2}><N8AO aoRadius={.7} intensity={1.4} distanceFalloff={1} halfRes/><Bloom mipmapBlur intensity={night?.17:.035} luminanceThreshold={1.3} luminanceSmoothing={.6}/></EffectComposer>
 </>;
}
class Boundary extends Component{state={error:false};static getDerivedStateFromError(){return{error:true};}render(){return this.state.error?<div className="error">Unable to open the 3D view. Refresh with WebGL enabled.</div>:this.props.children;}}
function App(){
 const[roof,setRoof]=useState(true),[floor,setFloor]=useState('All');
 const[night,setNight]=useState(false),[view,setView]=useState('Front'),[reset,setReset]=useState(0),[ready,setReady]=useState(false),[lights,setLights]=useState([]),[error,setError]=useState(''),[hide,setHide]=useState(false),[custom,setCustom]=useState(false);
 useEffect(()=>{fetch(`${import.meta.env.BASE_URL}two-storey/lighting.json?v=8`).then(r=>{if(!r.ok)throw Error('Lighting unavailable');return r.json();}).then(setLights).catch(e=>setError(e.message));const k=e=>{if(e.key.toLowerCase()==='h')setHide(v=>!v);if(e.key==='Escape')setHide(false)};window.addEventListener('keydown',k);return()=>window.removeEventListener('keydown',k);},[]);
 const onReady=React.useCallback(()=>setReady(true),[]),onMove=React.useCallback(()=>setCustom(true),[]);
 const choose=v=>{setView(v);setCustom(false);setReset(r=>r+1)};
 return <main className={`${night?'night':''} ${hide?'hide':''}`}><Boundary><Canvas shadows camera={{position:VIEWS.Front,fov:39,near:.1,far:250}} dpr={[1,1.5]} gl={{antialias:true,toneMapping:THREE.ACESFilmicToneMapping,toneMappingExposure:1.0}}><Scene {...{night,view,reset,onMove,onReady,lights,roof,floor}}/></Canvas></Boundary>
 <header><div className="identity"><b>FORM<span> / </span>02</b><small>KERALA RESIDENCE</small></div><div className="lighting"><button aria-pressed={!night} className={!night?'active':''} onClick={()=>setNight(false)}>☀ DAY</button><button aria-pressed={night} className={night?'active':''} onClick={()=>setNight(true)}>☾ NIGHT</button></div><button className="quiet" onClick={()=>document.documentElement.requestFullscreen?.().catch(()=>{})}>Fullscreen ⛶</button></header>
 <div className="view-label"><b>{custom?'EXPLORE':view.toUpperCase()} VIEW</b><span>{night?'Warm light / blue hour':'Tropical daylight'}</span></div>
 <footer><nav aria-label="Camera views">{Object.keys(VIEWS).map(v=><button key={v} aria-pressed={v===view&&!custom} className={v===view&&!custom?'active':''} onClick={()=>choose(v)}>{v.toUpperCase()}</button>)}</nav><div className="secondary"><button aria-pressed={!roof} onClick={()=>setRoof(v=>!v)}>Roof {roof?'on':'off'}</button>{['All','Ground','First'].map(f=><button key={f} aria-pressed={floor===f} className={floor===f?'active':''} onClick={()=>{setFloor(f);if(f!=='All'){setRoof(false);choose('Top / Floor');}}}>{f} floors</button>)}<button onClick={()=>choose('Front')}>↺ Reset</button><button onClick={()=>setHide(true)}>Hide UI</button></div></footer>
 <div className="hint">DRAG TO ORBIT · SCROLL TO ZOOM · RIGHT-DRAG TO PAN</div><div className="status">{error||'REFERENCE STUDY / TWO STOREYS'}</div>
 {hide&&<button className="restore" onClick={()=>setHide(false)}>Show controls · H</button>}
 {(!ready||!lights.length)&&<div className="loading">{error||'Preparing the residence…'}<small>Architecture, interiors & tropical gardens</small></div>}
 </main>;
}
createRoot(document.getElementById('root')).render(<App/>);
