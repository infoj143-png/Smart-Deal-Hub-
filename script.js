// ===============================
// Smart Deal Hub Script v1.0
// ===============================

// Dark / Light Mode

const themeBtn = document.getElementById("themeBtn");

themeBtn.addEventListener("click", () => {

    document.body.classList.toggle("dark");

    if(document.body.classList.contains("dark")){

        themeBtn.innerHTML="☀️";

        localStorage.setItem("theme","dark");

    }else{

        themeBtn.innerHTML="🌙";

        localStorage.setItem("theme","light");

    }

});

// Load Saved Theme

window.onload=()=>{

    if(localStorage.getItem("theme")==="dark"){

        document.body.classList.add("dark");

        themeBtn.innerHTML="☀️";

    }

}

// ===============================
// Search Feature
// ===============================

const search=document.querySelector(".hero input");

search.addEventListener("keyup",function(){

const keyword=this.value.toLowerCase();

const cards=document.querySelectorAll(".card");

cards.forEach(card=>{

const text=card.innerText.toLowerCase();

if(text.includes(keyword)){

card.style.display="block";

}else{

card.style.display="none";

}

});

});

// ===============================
// Smooth Scroll
// ===============================

document.querySelectorAll('a[href^="#"]').forEach(anchor=>{

anchor.addEventListener("click",function(e){

e.preventDefault();

document.querySelector(this.getAttribute("href"))

.scrollIntoView({

behavior:"smooth"

});

});

});

// ===============================
// Reveal Animation
// ===============================

const observer=new IntersectionObserver(entries=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

entry.target.style.opacity=1;

entry.target.style.transform="translateY(0)";

}

});

});

document.querySelectorAll(".card").forEach(card=>{

card.style.opacity=0;

card.style.transform="translateY(40px)";

card.style.transition=".7s";

observer.observe(card);

});

// ===============================
// Newsletter
// ===============================

const subscribeBtn=document.querySelector("#newsletter button");

subscribeBtn.addEventListener("click",()=>{

const email=document.querySelector("#newsletter input").value;

if(email===""){

alert("Please enter your email.");

return;

}

alert("Thank you for subscribing!");

document.querySelector("#newsletter input").value="";

});

// ===============================
// Back To Top Button
// ===============================

const topBtn=document.createElement("button");

topBtn.innerHTML="⬆";

topBtn.id="topBtn";

document.body.appendChild(topBtn);

topBtn.style.position="fixed";
topBtn.style.bottom="20px";
topBtn.style.right="20px";
topBtn.style.padding="15px";
topBtn.style.border="none";
topBtn.style.borderRadius="50%";
topBtn.style.cursor="pointer";
topBtn.style.display="none";
topBtn.style.background="#2563eb";
topBtn.style.color="white";
topBtn.style.fontSize="20px";

window.addEventListener("scroll",()=>{

if(window.scrollY>300){

topBtn.style.display="block";

}else{

topBtn.style.display="none";

}

});

topBtn.addEventListener("click",()=>{

window.scrollTo({

top:0,

behavior:"smooth"

});

});

// ===============================
// Console Message
// ===============================

console.log("Smart Deal Hub Loaded Successfully 🚀");
