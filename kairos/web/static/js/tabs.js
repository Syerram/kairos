/*
 * Simple Tabs script
 * Requires jQuery
 *
 * Author: bert.devriese@gmail.com http://www.bertdevriese.be
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