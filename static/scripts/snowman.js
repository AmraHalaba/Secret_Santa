let circle = document.getElementById("snowman");

const onMouseMove = (e) => {
  circle.style.left = e.pageX + "px";
  circle.style.top = e.pageY + "px";
};
document.addEventListener("mousemove", onMouseMove);
