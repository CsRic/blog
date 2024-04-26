function navigateTo(page) {
    window.location.href = "../../" + page;
}

function getCurrentPage() {
    var path = window.location.pathname;
    var diaryIndex = path.indexOf('/diary/');
    return diaryIndex !== -1 ? path.substring(diaryIndex + '/diary/'.length) : '';
}

function setupNavigationButtons(pages) {
    var currentPage = getCurrentPage();
    var currentIndex = pages.indexOf(currentPage);
    var prevBtn = document.getElementById('prev');
    var nextBtn = document.getElementById('next');

    if (currentIndex < pages.length - 1) {
        prevBtn.addEventListener('click', function() { navigateTo(pages[currentIndex + 1]); });
    } else {
        prevBtn.classList.add('disabled');
    }

    if (currentIndex > 0) {
        nextBtn.addEventListener('click', function() { navigateTo(pages[currentIndex - 1]); });
    } else {
        nextBtn.classList.add('disabled');
    }
}

// Sidebar logic
function updateSidebar() {
    var headings = document.querySelectorAll('#markdown_content h2, #markdown_content h3, #markdown_content h4, #markdown_content h5');
    var sidebarList = document.getElementById('sidebar_list');
    headings.forEach(function(heading) {
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.textContent = heading.textContent;
        a.href = '#' + heading.id;
        a.style.textDecoration = 'none';
        var level = parseInt(heading.tagName.substring(1));
        li.style.marginLeft = (level - 1) + 'rem'; 
        li.appendChild(a);
        sidebarList.appendChild(li);
    });
}

// Event listeners for header and home link
function setupHeaderAndHomeLinks() {
    var head = document.getElementById('head');
    head.addEventListener('click', function () {
        window.top.location.href = window.location.href;
    });
    var home = document.getElementById('home');
    home.addEventListener('click', function () {
        window.top.location.href = "../../../../index.html";
    });
}

// Load pages and setup buttons
function loadPagesAndSetupButtons() {
    fetch("../../time_index.json")
        .then(response => response.json())
        .then(pages => setupNavigationButtons(pages))
        .catch(error => console.error('Error loading pages:', error));
}

function updateRightColumnMarginLeft() {
    var rightColumns = document.querySelectorAll('.right-column');
    rightColumns.forEach(function(column) {
        var newMarginLeft = 'calc(20% + 12px)';
        column.style.marginLeft = newMarginLeft;
    });
}


// Initialization on DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    setupHeaderAndHomeLinks();
    loadPagesAndSetupButtons();
    updateSidebar();
    updateRightColumnMarginLeft();
    window.addEventListener('resize', updateRightColumnMarginLeft);
});