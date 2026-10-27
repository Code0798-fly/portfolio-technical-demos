const threshold = 2000;
const cart = [];
const money = value => `₹${value.toLocaleString("en-IN")}`;
const total = () => cart.reduce((sum, item) => sum + item.price, 0);

function render() {
  const subtotal = total();
  document.querySelector("#items").innerHTML = cart.length
    ? cart.map((item, index) => `<div class="item"><span>${item.name}</span><span>${money(item.price)} <button class="remove" data-index="${index}" aria-label="Remove ${item.name}">×</button></span></div>`).join("")
    : "<p class='empty'>Your cart is empty.</p>";
  document.querySelector("#count").textContent = `${cart.length} ${cart.length === 1 ? "item" : "items"}`;
  document.querySelector("#total").textContent = money(subtotal);
  document.querySelector("#progress").style.width = `${Math.min(100, subtotal / threshold * 100)}%`;
  document.querySelector("#threshold-copy").textContent = subtotal >= threshold ? "You unlocked free delivery." : `${money(threshold - subtotal)} away from free delivery.`;
  document.querySelector("#upsell").hidden = subtotal === 0 || subtotal >= threshold || cart.some(item => item.name === "Travel pouch");
  document.querySelectorAll(".remove").forEach(button => button.addEventListener("click", () => { cart.splice(button.dataset.index, 1); render(); }));
}

document.querySelectorAll(".product").forEach(button => button.addEventListener("click", () => {
  cart.push({ name: button.dataset.name, price: Number(button.dataset.price) }); render();
}));
document.querySelector("#upsell-button").addEventListener("click", () => { cart.push({ name: "Travel pouch", price: 499 }); render(); });
render();
