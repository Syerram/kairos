/*
 * Simple Tabs script
 * Requires jQuery
 *
 * Author: <bert.devriese@gmail.com> - http://www.bertdevriese.be
 */

function tab_open(tabname, context)
{
	var $parent = $(context).parentsUntil('.tab-box').parent().first();
	
	// Highlight Correct Tab
	$parent.find('.tabs > li').removeClass('active');
	$(context).parent().addClass('active');
	 	
	// Show Tab Content Container
	$parent.find('.tab-content').hide().filter('#'+tabname).show();
}


/*
 * Simple Hanging Box script
 * Requires jQuery
 *
 * Author: <bert.devriese@gmail.com> - http://www.bertdevriese.be
 */
function hanging_box_toggle(context)
{
	$('body').toggleClass('hanging-box-active');
	
	if ($('body').hasClass('hanging-box-active'))
	{
		$(context).removeClass('arrow-right').addClass('arrow-left');
	}
	else 
	{
		$(context).removeClass('arrow-left').addClass('arrow-right');
	}
}


/*
 * Simple comments toggle script
 * Requires jQuery
 *
 * Author: <bert.devriese@gmail.com> - http://www.bertdevriese.be
 */
function comments_toggle(context)
{
	$(context).parentsUntil('.box').parent().find('div.comments').slideToggle('fast');
	$(context).parentsUntil('.box').parent().find('.button.comments').toggleClass('active');
}