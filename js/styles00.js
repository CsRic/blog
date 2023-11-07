function updateMargin() {
    // 获取.header元素的高度
    var element  = document.querySelector('.title-container')
    var rect = element.getBoundingClientRect();
    var scrollTop = document.documentElement.scrollTop;
    var elementBottom = rect.bottom + scrollTop;
    var topHeight = (elementBottom > scrollTop ? elementBottom : 2);
    document.querySelector('.left-column').style.top = topHeight + 'px';
    var headerHeight = document.querySelector('.title-container').offsetHeight;
}

window.onload = updateMargin;
window.onresize = updateMargin;
window.onscroll = updateMargin;