/* =========================================
   ECO Plus Diagnostic Center
   Frontend JavaScript
   ========================================= */

document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menuToggle");
    const mainNav = document.getElementById("mainNav");

    if (menuToggle && mainNav) {
        menuToggle.addEventListener("click", () => {
            const isOpen = mainNav.classList.toggle("active");
            menuToggle.setAttribute("aria-expanded", String(isOpen));
            menuToggle.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
            menuToggle.textContent = isOpen ? "✕" : "☰";
        });

        const navLinks = mainNav.querySelectorAll("a");
        navLinks.forEach((link) => {
            link.addEventListener("click", () => {
                mainNav.classList.remove("active");
                menuToggle.setAttribute("aria-expanded", "false");
                menuToggle.setAttribute("aria-label", "Open menu");
                menuToggle.textContent = "☰";
            });
        });
    }

    const appointmentForm = document.getElementById("appointmentForm");
    const formMessage = document.getElementById("formMessage");

    if (appointmentForm) {
        appointmentForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            if (formMessage) {
                formMessage.textContent = "⏳ অনুগ্রহ করে অপেক্ষা করুন...";
                formMessage.className = "form-message";
            }

            const formData = new FormData(appointmentForm);
            const data = {
                name: formData.get("name"),
                phone: formData.get("phone"),
                service: formData.get("service")
            };

            if (!data.name || !data.phone || !data.service) {
                showMessage("⚠️ সব তথ্য পূরণ করুন।", "error");
                return;
            }

            try {
                const response = await fetch("/api/appointments", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    body: JSON.stringify(data)
                });

                let result = {};
                try {
                    result = await response.json();
                } catch {
                    result = {};
                }

                if (!response.ok) {
                    throw new Error(result.message || "Appointment request failed.");
                }

                showMessage(result.message || "✅ আপনার Appointment Request সফলভাবে পাঠানো হয়েছে।", "success");
                appointmentForm.reset();
            } catch (error) {
                console.error("Appointment Error:", error);
                showMessage("❌ এখন Appointment পাঠানো যাচ্ছে না। পরে আবার চেষ্টা করুন।", "error");
            }
        });
    }

    function showMessage(message, type) {
        if (!formMessage) return;
        formMessage.textContent = message;
        formMessage.className = `form-message ${type}`;
    }

    const internalLinks = document.querySelectorAll('a[href^="#"]');
    internalLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            const targetId = link.getAttribute("href");
            if (!targetId || targetId === "#") return;

            const target = document.querySelector(targetId);
            if (target) {
                event.preventDefault();
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        });
    });

    const phoneInput = document.getElementById("phone");
    if (phoneInput) {
        phoneInput.addEventListener("input", () => {
            phoneInput.value = phoneInput.value.replace(/[^\d০-৯+ -]/g, "");
        });
    }

    const currentYear = new Date().getFullYear();
    const copyright = document.querySelector(".copyright");
    if (copyright) {
        copyright.innerHTML = `© ${currentYear} ECO Plus Diagnostic Center. All rights reserved.`;
    }
});
