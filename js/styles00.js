function updateMargin() {
    // 获取.header元素的高度
    var headerHeight = document.querySelector('.title-container').offsetHeight + 1;
  
    // 设置.left-column的top属性，确保它距离.header底部一定距离
    document.querySelector('.left-column').style.top = headerHeight + 'px';
    document.querySelector('.right-column').style.paddingTop = headerHeight + 'px';
}

window.onload = updateMargin;
window.onresize = updateMargin;