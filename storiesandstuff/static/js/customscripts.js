console.log('custom scripts loaded');
function takeCareOfErrors(error_str)
	{
		if(error_str=='') return false;
		else showModal_k("Error",error_str);
	}
function showModal_k2(titlemessage="no title",bodymessage="Dang it Kitchu.. Pull yourself together ")
		{
		 $('#mheader').html(titlemessage);
		 $('#mmessage').html(bodymessage);
		 $('#mm').modal();
		}

