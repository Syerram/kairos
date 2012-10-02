/*
 * Simple placeholder fix script
 * Requires jQuery
 *
 * Author: bert.devriese@gmail.com http://www.bertdevriese.be
 */

$(document).ready(function ()
{
	// Check for placeholder support
	var element = document.createElement('input');
    
	if (!('placeholder' in element))
    {
    	// No support => Manual implementation
    	$('input[placeholder]')
    		.each(function ()
    		{
    			$(this).val($(this).attr('placeholder'));
    		})
	    	.focus(function ()
	    	{
	    		if ($(this).val() == $(this).attr('placeholder'))
	    		{
	    			$(this).val('');
	    		}
	    	})
	    	.blur(function () 
	    	{
	    		if ($(this).val() == '')
	    		{
	    			$(this).val($(this).attr('placeholder'));
	    		}
	    	});
    }
});