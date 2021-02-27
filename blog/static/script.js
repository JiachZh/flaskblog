
$(document).ready(function() {
  (function() {
    var query = document.querySelector('.bricklayer');
    if(query !== null) {
      var bricklayer = new Bricklayer(document.querySelector('.bricklayer'));
    }
  })();
  $('textarea#Content').summernote({
    height: 300
  });
  $('a.post_url').attr({
    href: '/pos' + window.location.pathname.slice(4)
  }).text('/pos' + window.location.pathname.slice(4));
  $('input.post_url').attr({
    value: '/pos' + window.location.pathname.slice(4)
  });
  $('#submit-new-comment').click(event =>{
    event.preventDefault();
    var $txt = $('#new-comment');
    var data = new URLSearchParams();
    data.append('PostId', $txt.attr('data-post-id'));
    data.append('Content', $txt.val());
    $('#submit-new-comment').addClass('disabled')
    $('input,textarea').attr('disabled', true);

    fetch('/comment', {
      body: data,
      method: 'POST',
      headers: new Headers({
        "Content-Type": "application/x-www-form-urlencoded"
      })
    }).then(data => {
      location.reload();
    }).catch(err => alert(err));
  });
  $('.cite-comment').click(event => {
    event.preventDefault();
    $('#new-comment').append('\n#comment-' + $(event.target).attr('data-comment-id'));
  });
  $('.delete-comment').click(event => {
    event.preventDefault();
    var data = new URLSearchParams();
    data.append('CommentId', $(event.target).attr('data-comment-id'));
    data.append('Delete', 1);
    fetch('/comment', {
      body: data,
      method: 'POST',
      headers: new Headers({
        "Content-Type": "application/x-www-form-urlencoded"
      })
    }).then(data => {
      location.reload();
    }).catch(err => alert(err));
  });
  $('.edit-comment').click(event => {
    event.preventDefault();
    var commentId = $(event.target).attr('data-comment-id');
    $('#CommentEditor').val($('p[data-comment-id=' + commentId + ']').text())
    $('#submit-updated-comment').attr('data-comment-id', commentId);
    $('#submit-updated-comment').off();
    $('#submit-updated-comment').click(event => {
      var $txt = $('#CommentEditor');
      var data = new URLSearchParams();
      data.append('CommentId', $(event.target).attr('data-comment-id'));
      data.append('PostId', $('#new-comment').attr('data-post-id'));
      data.append('Content', $(CommentEditor).val());
      fetch('/comment', {
        body: data,
        method: 'POST',
        headers: new Headers({
          "Content-Type": "application/x-www-form-urlencoded"
        })
      }).then(data => {
        location.reload();
      }).catch(err => alert(err));
    });
    $('#EditCommentModal').modal('show');
  });
  $('.comments :not(script)').contents().filter(function() {
    return this.nodeType === 3;
  }).replaceWith(function() {
    return this.nodeValue.replace(/(#comment-\d+)/g,'<a href="$1">$1</a>');
  });
  $('.my-rating>span').hover(function() {
    var star = $(this).attr('data-star');
    $('.my-rating>span').each(function(idx) {
      if(star > idx) {
        $(this).css({
          color: '#fdca15'
        });
      } else {
        $(this).css({
          color: 'rgb(154, 154, 154)'
        });
      }
    });
  }, function() {
    $('.my-rating>span').css({
      color: ''
    });
  }).click(event => {
    var data = new URLSearchParams();
    data.append('PostId', $('#new-comment').attr('data-post-id'));
    data.append('Content', $(event.target).attr('data-star'));
    fetch('/rating', {
      body: data,
      method: 'POST',
      headers: new Headers({
        "Content-Type": "application/x-www-form-urlencoded"
      })
    }).then(data => {
      location.reload();
    }).catch(err => alert(err));
  });
  $('#remove-rating').click(event => {
    var data = new URLSearchParams();
    data.append('PostId', $('#new-comment').attr('data-post-id'));
    data.append('Delete', '1');
    fetch('/rating', {
      body: data,
      method: 'POST',
      headers: new Headers({
        "Content-Type": "application/x-www-form-urlencoded"
      })
    }).then(data => {
      location.reload();
    }).catch(err => alert(err));
  });
  $('#tag-post').click(event => {
    var data = new URLSearchParams();
    data.append('PostId', $('#new-comment').attr('data-post-id'));
    fetch('/tagging', {
      body: data,
      method: 'POST',
      headers: new Headers({
        "Content-Type": "application/x-www-form-urlencoded"
      })
    }).then(data => {
      location.reload();
    }).catch(err => alert(err));
  });
  $('#untag-post').click(event => {
    var data = new URLSearchParams();
    data.append('PostId', $('#new-comment').attr('data-post-id'));
    data.append('Delete', '1');
    fetch('/tagging', {
      body: data,
      method: 'POST',
      headers: new Headers({
        "Content-Type": "application/x-www-form-urlencoded"
      })
    }).then(data => {
      location.reload();
    }).catch(err => alert(err));
  });
  $('#sort-newest-first').click(() => {
    $('#all-posts>tbody tr').sort((a, b) => new Date($(b).find('.created-at').text()) - new Date($(a).find('.created-at').text())).appendTo('#all-posts>tbody');
    $('#sort-newest-first').toggleClass('btn-secondary btn-outline-secondary');
    $('#sort-oldest-first').toggleClass('btn-secondary btn-outline-secondary');
  });
  $('#sort-oldest-first').click(() => {
    $('#all-posts>tbody tr').sort((a, b) => new Date($(a).find('.created-at').text()) - new Date($(b).find('.created-at').text())).appendTo('#all-posts>tbody');
    $('#sort-newest-first').toggleClass('btn-secondary btn-outline-secondary');
    $('#sort-oldest-first').toggleClass('btn-secondary btn-outline-secondary');
  });
  var keywords = $('.search-keywords').text();
  if(typeof keywords === 'string' && keywords.length === 0) {
    $('.search-result').remove();
  }
  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
  }
  $('.search-post').each(function(idx) {
    if($(this).find('h3').text().toLowerCase().includes(keywords.toLowerCase()) || $(this).find('p').text().toLowerCase().includes(keywords.toLowerCase())) {
      $(this).find('h3').html($(this).find('h3').text().replace(new RegExp('(' + escapeRegExp(keywords) + ')', 'gi'), '<span class="search-matched">$1</span>'));
      var text = $(this).find('p').text();
      var len = text.length;
      var regex = new RegExp('(' + escapeRegExp(keywords) + ')', 'gi');
      $(this).find('p').replaceWith(Array.from(text.matchAll(regex)).map(m => '<p>..' + text.slice(Math.max(0, m.index - 7), Math.min(m.index + 12, len)) + '...</p>').map(m => m.replace(new RegExp('(' + escapeRegExp(keywords) + ')', 'gi'), '<span class="search-matched">$1</span>')))
    } else {
      $(this).remove();
    }
  });
  $('.search-result').removeClass('invisible')
  $('.untag-post').click(event => {
    var data = new URLSearchParams();
    data.append('PostId', $(event.target).attr('data-post-id'));
    data.append('Delete', '1');
    fetch('/tagging', {
      body: data,
      method: 'POST',
      headers: new Headers({
        "Content-Type": "application/x-www-form-urlencoded"
      })
    }).then(data => {
      location.reload();
    }).catch(err => alert(err));
  });
});
