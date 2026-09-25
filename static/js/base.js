document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");
    const menuToggle = document.getElementById("menuToggle");


    /*
    ========================================
    MOBILE SIDEBAR
    ========================================
    */

    if (menuToggle && sidebar) {

        menuToggle.addEventListener("click", function () {

            sidebar.classList.toggle("open");

        });

    }


    /*
    ========================================
    CLOSE SIDEBAR AFTER MOBILE NAVIGATION
    ========================================
    */

    const navItems = document.querySelectorAll(".nav-item");

    navItems.forEach(function (item) {

        item.addEventListener("click", function () {

            if (window.innerWidth <= 800) {

                sidebar.classList.remove("open");

            }

        });

    });


    /*
    ========================================
    SITE SELECTOR
    ========================================
    */

    const siteSelector =
        document.getElementById("siteSelector");

    if (siteSelector) {

        siteSelector.addEventListener("change", function () {

            this.form.submit();

            /*
            По-късно тук можем да добавим:

            - Django request
            - URL параметър
            - AJAX
            - запазване на избрания site
            */

        });

    }

});