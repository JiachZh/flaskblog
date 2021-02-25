
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
});
