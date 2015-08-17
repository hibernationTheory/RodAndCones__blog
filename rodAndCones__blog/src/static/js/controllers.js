var App = angular.module('blogApp');

App.directive('shortenChildPText', function() {
  return {
    link:function($scope, element, attrs) {
      $scope.$evalAsync(function() {
        shortenChildPText(element);
      })
    }
  }
});

App.controller('searchFilter', function($scope, $element) {
  var elementCategory = $element.data('item-category');
  console.log(elementCategory);
  this.category = elementCategory;
  $scope.showElement = showElement;
})

var showElement = function(query, selection, id) {
  var element = document.getElementById(id);
  var el_category = element.dataset.itemCategory;
  var el_name = element.dataset.itemName;
  var el_name = el_name.toLowerCase();

  var match_selection;
  var match_query;

  if (!query && !selection) {
    return true;
  }

  if (selection) {
    if (selection.toLowerCase().trim() === el_category.toLowerCase().trim()) {
      match_selection = true;
    } else {
      match_selection = false;
    }
  } else {
    match_selection = true;
  }

  if (query) {
    var query = query.toLowerCase();
    if (el_name.indexOf(query) !== -1) {
        match_query = true;
    } else {
      match_query = false;
    }
  } else {
    match_query = true;
  }

  if ( match_query && match_selection ) {
    return true;
  } else {
    return false;
  }
}

App.controller('itemContainer', function($scope, $element) {
  // not using this for now, it displays the child count not at the same things get hidden. 
  // (but one item later)
  var childrenCount = $element.get(0).childElementCount;

  $scope.$watch(function() {
    var children = $element.get(0).childNodes;
    var topicItems = 0;
    var hiddenItems = 0;

    for (var i = 0; i < children.length; i++) {
      var node = children[i];
      if (node.className && node.className.indexOf("topic-item") !== -1) {
        topicItems += 1;
        if (node.className.indexOf("ng-hide") !== -1 ) {
          hiddenItems += 1;
        }
      }
    }
    if (topicItems == hiddenItems) {
      console.log('allHidden');
    }
  });
});


var shortenChildPText = function(element) {
  // defunct and is not in use, doing this in backend now
  // keeping it for reference purposes in case a directive
  // that alters text is needed.
  var $el, blockquote, $title, $paragraph;
  var nodeContentType;
  var parentEl = element[0];
  var $parentEl = $(parentEl);
  var $postContent = $parentEl.find(".post-content");
  var $newContent;

  var $firstChild = $postContent.children().first();
  var nodeName = $firstChild.get(0).nodeName;

  if (nodeName === "BLOCKQUOTE") {
    blockquote = true;
    $el = $firstChild;
  } else if (nodeName === "H1") {
    $title = $firstChild;
    $paragraph = $postContent.children().first('p');
    $el = $paragraph;
  } else {
    return false;
  }
  console.log($el);
  var el = $el.get(0);

  var text = el.innerText;
  console.log(text)
  if (text) {
    var words = text.split(" ");
    if (nodeContentType === 'P') {
      limitWord = 20
    } else {
      limitWord = 30
    }
    var newText = words.splice(0, limitWord).join(" ");
    newText = newText + "...";
  } else {
    return null;
  }

  if (blockquote) {
      $newContent = $("<blockquote>A</blockquote>");
    } else if ($title) {
      $newContent = $("<h1>A</h1>");
      $newContent.append($("<p>" + newText + "</p>"));
  }

  $parentEl.html($newContent.get(0).outerHTML);
}

