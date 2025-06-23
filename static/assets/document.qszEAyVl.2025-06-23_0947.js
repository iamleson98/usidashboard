import{d as g,r as s,G as i,H as l,c,a6 as f,u as d,O as b,t as _,ag as m,o as t,a,J as y}from"./@vue.BDy9tIRg.2025-06-23_0947.js";const k=["innerHTML"],T=["innerHTML"],v=["src","alt"],M=g({__name:"document",setup(w){const o=s([{title:"Project objective",shortDesc:"The main dashboard for managing abnormal checking time, production line heads count by realtime",content:""},{title:"Authors",content:`
    Yunfu Xiang - Test department leader, project manager <br />
    Nickson Le - nickson_le@usiglobal.com (core maintainer) <br />
    Mac Pham - Supporter <br />
    Mark do - Supporter`,shortDesc:"List of employees who created this web app"},{title:"Abnormals listing page",content:`
    1) The standard time for a person to leave the production line is 10 minutes. <br />
    2) The standard time for meal taking are specified specifically for each departments.<br />

    If the duration between the checking out and the checking in timestamps of an employee is exceed the standard alowed minutes, that is considered abnormals. <br />
    `,shortDesc:"The interface for managers to easily finding abnormal checking records, by employee ID, departments, floor, by dates range, ...",img:"/images/image.png"},{title:"Realtime dashboard page",shortDesc:"The realtime dashboard for managers to know how many people are actively working inside each floor, and the latest abnormal cases recorded.",content:`
    1) The chart section showing the latest 10 history records of number of employees, staying inside of each production lines on each floor. The chart is realtime updated every 20 seconds. <br />
    2) The abnormal table showing latest 50 abnormal checking records, sorting by cheking time, most recent cases first. The table data is updated every 20 seconds. <br />
    `}]),n=s(o.value[0].title);return(L,r)=>{const h=m("el-collapse-item"),p=m("el-collapse");return t(),i(p,{modelValue:d(n),"onUpdate:modelValue":r[0]||(r[0]=e=>_(n)?n.value=e:null),accordion:""},{default:l(()=>[(t(!0),c(b,null,f(d(o),(e,u)=>(t(),i(h,{key:u,title:e.title,name:e.title},{default:l(()=>[a("div",{innerHTML:e.shortDesc},null,8,k),a("div",{innerHTML:e.content},null,8,T),a("div",null,[a("div",null,[e.img?(t(),c("img",{key:0,src:e.img,alt:e.title},null,8,v)):y("",!0)])])]),_:2},1032,["title","name"]))),128))]),_:1},8,["modelValue"])}}});export{M as default};
