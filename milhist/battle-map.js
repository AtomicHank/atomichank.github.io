document.addEventListener("DOMContentLoaded", function () {
  var maps = document.querySelectorAll("[data-battle-map]");

  maps.forEach(function (root) {
    var steps = Array.from(root.querySelectorAll("[data-phase-step]"));
    var phases = Array.from(root.querySelectorAll("[data-phase]"));
    var status = root.querySelector("[data-phase-status]");
    var previousButton = root.querySelector("[data-map-prev]");
    var nextButton = root.querySelector("[data-map-next]");
    var playButton = root.querySelector("[data-map-play]");
    var currentPhase = 1;
    var timerId = null;

    if (!steps.length || !phases.length || !status) {
      return;
    }

    function stopPlayback() {
      if (timerId !== null) {
        window.clearInterval(timerId);
        timerId = null;
      }

      if (playButton) {
        playButton.textContent = "Play";
        playButton.setAttribute("aria-pressed", "false");
      }
    }

    function renderPhase(phaseNumber) {
      currentPhase = phaseNumber;

      phases.forEach(function (phase) {
        var isActive = Number(phase.getAttribute("data-phase")) === phaseNumber;
        phase.classList.toggle("is-active", isActive);
      });

      steps.forEach(function (step) {
        var isActive = Number(step.getAttribute("data-phase-step")) === phaseNumber;
        step.classList.toggle("is-active", isActive);
      });

      var activeStep = root.querySelector(
        '[data-phase-step="' + phaseNumber + '"]'
      );

      if (activeStep) {
        status.textContent = activeStep.getAttribute("data-phase-title") || "";
      }

      if (previousButton) {
        previousButton.disabled = phaseNumber === 1;
      }

      if (nextButton) {
        nextButton.disabled = phaseNumber === steps.length;
      }
    }

    function movePhase(direction) {
      var nextPhase = Math.min(
        steps.length,
        Math.max(1, currentPhase + direction)
      );
      renderPhase(nextPhase);
    }

    function startPlayback() {
      if (timerId !== null) {
        stopPlayback();
        return;
      }

      if (currentPhase === steps.length) {
        renderPhase(1);
      }

      if (playButton) {
        playButton.textContent = "Pause";
        playButton.setAttribute("aria-pressed", "true");
      }

      timerId = window.setInterval(function () {
        if (currentPhase === steps.length) {
          stopPlayback();
          return;
        }

        renderPhase(currentPhase + 1);
      }, 2600);
    }

    if (previousButton) {
      previousButton.addEventListener("click", function () {
        stopPlayback();
        movePhase(-1);
      });
    }

    if (nextButton) {
      nextButton.addEventListener("click", function () {
        stopPlayback();
        movePhase(1);
      });
    }

    if (playButton) {
      playButton.addEventListener("click", startPlayback);
    }

    renderPhase(1);
  });
});
