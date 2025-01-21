// script.js
const canvas = document.getElementById("dynamic-bg");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const colors = ["#ff6a00", "#f9d423", "#6a11cb", "#2575fc"];
const circles = [];

function Circle() {
  this.x = Math.random() * canvas.width;
  this.y = Math.random() * canvas.height;
  this.radius = Math.random() * 80 + 20;
  this.color = colors[Math.floor(Math.random() * colors.length)];
  this.dx = Math.random() * 2 - 1;
  this.dy = Math.random() * 2 - 1;

  this.draw = function () {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.fill();
    ctx.closePath();
  };

  this.update = function () {
    if (this.x + this.radius > canvas.width || this.x - this.radius < 0) {
      this.dx = -this.dx;
    }
    if (this.y + this.radius > canvas.height || this.y - this.radius < 0) {
      this.dy = -this.dy;
    }

    this.x += this.dx;
    this.y += this.dy;

    this.draw();
  };
}

for (let i = 0; i < 50; i++) {
  circles.push(new Circle());
}

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  circles.forEach((circle) => circle.update());
  requestAnimationFrame(animate);
}

animate();

window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});