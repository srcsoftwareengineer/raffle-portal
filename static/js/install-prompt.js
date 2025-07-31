let deferredPrompt;
const installBtn = document.createElement("button");
installBtn.innerText = "📲 Adicione Tô Rifando na sua tela!";
installBtn.style = `
  position:fixed;
  bottom:20px;
  left:20px;
  padding:10px 20px;
  background:#28a745;
  color:white;
  border:none;
  border-radius:5px;
  z-index:9999;
`;
installBtn.hidden = true;

window.addEventListener("beforeinstallprompt", (e) => {
  e.preventDefault();
  deferredPrompt = e;
  document.body.appendChild(installBtn);
  installBtn.hidden = false;

  installBtn.addEventListener("click", async () => {
    installBtn.hidden = true;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    console.log("[StormPWA] Instalação: ", outcome);
    deferredPrompt = null;
  });
});

