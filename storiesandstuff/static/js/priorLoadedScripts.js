function showModal_k(titlemessage="no title",bodymessage="Dang it Kitchu.. Pull yourself together ")
		{
		 $('#mheader').html(titlemessage);
		 $('#mmessage').html(bodymessage);
		 $('#mm').modal();
		}

		/*
function fixsubBtn()
	{
		var subB=document.querySelector('#subBtn');
		subB.addEventListener('click',
								       function ()
								       {
								       	
								       	showModal_k("Info","Success");
								       	
								       }
			                 );
	}
*/
function delx(elem)
	{
		//kmhere
		//write the functionality to remove both the button and the textbox
		let textboxes=document.getElementsByClassName('tb');
		let debuttons=document.getElementsByClassName('tbb');
		for(var i=0;i<textboxes.length;i++)
			{
				if(debuttons[i]==elem)
				{
					debuttons[i].remove();
					textboxes[i].remove();
				}
			}

		let imboxes=document.getElementsByClassName('imx');
		debuttons=document.getElementsByClassName('imtbb');
		varybuttons=document.getElementsByClassName('rtbb');
		for(var i=0;i<imboxes.length;i++)
			{
				if(debuttons[i]==elem)
				{
					debuttons[i].remove();
					imboxes[i].remove();
					varybuttons[i].remove();
				}
			}
	}



function store_vals_temp(celem)
	{
		let texElems=document.getElementsByClassName(celem);
		let vals_in_texboxes=[];
		for(var i =0;i<texElems.length;i++)
			{
				vals_in_texboxes.push(texElems[i].value);
			}
		return vals_in_texboxes;
	}
function reinstate_vals(celem,vals_in_texboxes)
	{
		let texElems=document.getElementsByClassName(celem);
		for(var i =0;i<texElems.length;i++)
			{
				if(vals_in_texboxes[i])
				texElems[i].value=vals_in_texboxes[i];
			}
	}

function takeComponentCount()
	{
		let elems=document.getElementsByClassName('addedElem');
		let componentList=[];
		for (var i=0;i<elems.length;i++)
			{
				if(elems[i].dataset.typex=='tb')
				{
					componentList.push({"type":"textbox","content":elems[i].value});
				}
				else if(elems[i].dataset.typex=='im')
				{
					componentList.push({"type":"image","content":elems[i].src,"width":elems[i].width});
				}
			}
			storeToCookie(componentList);

			let title=document.querySelector('#storytitle').value;
			let genre=document.querySelector('#storyGenre').value;
		    storeToCookie({"title":title,"genre":genre},"gtitle");	

	}
function makeSubmitAddTextAddImbtnsVisible()
	{
		document.querySelector('#toolButtons').style.display="";
		// document.querySelector('#subBtn').style.display="";
	}
function recreateWork(imgstrr="")
	{
		let x=retrieveCookie('storex');
		// console.log(x);
		if(x)
			{
				x=JSON.parse(x);

				
				if(x.length!=0)
				makeSubmitAddTextAddImbtnsVisible();

				let html_content='';
				for(var i=0;i<x.length;i++)
					{
						if(x[i].type=="textbox")
						html_content+=
						 `<div><textarea rows='5' cols='100' class='tb addedElem' data-typex='tb'>
						   ${x[i].content}
						  </textarea>
						  <br/><button class='btn btn-danger tbb' onclick='delx(this)'>delete</button>
						  </div>`;
						else

						{
						if(x[i].width)
						html_content+=
							 `<div>    <image 
							           class='imx addedElem' data-typex='im' 
							           src="${x[i].content}" 
							           width=${x[i].width} />`;
				        else
				        	html_content+=
							 `<div>    <image 
							           class='imx addedElem' data-typex='im' 
							           src="${x[i].content}" 
							           />`;
						html_content+=`<br/><button class='btn btn-danger imtbb' onclick='delx(this)'>delete</button>
						<br/><input type="range" 
						            class="rtbb" 
						            value="100" 
						            min="0" 
						            data-imval=0 
						            max="100" onchange="varyImage(this)"/>
						      </div>`;}

					}
				if(imgstrr!='')
					{
						html_content+=
						      `<div><image class='imx addedElem' data-typex='im' src="${imgstrr}" />
						<br/><button class='btn btn-danger imtbb' onclick='delx(this)'>delete</button>
						<br/><input type="range" class="rtbb" data-imval=0 value="100" min="0" max="100" onchange="varyImage(this)"/>
						       </div>`;
					}
				// console.log(html_content);
				document.querySelector("#workspace").innerHTML+=html_content;
				storeToCookie([]);
			}	
		x=retrieveCookie('gtitle');
		// console.log("here is the gtitle cookie:"+x);
		if(x)
			{
				x=JSON.parse(x);
				if(x.title.trim()!='')
				document.querySelector('#storytitle').value=x.title;
			    if(x.genre.trim()!='')
				document.querySelector('#storyGenre').value=x.genre;

			}
		storeToCookie({"title":'',"genre":''},"gtitle");	
	}

function varyImage(elem)
	{console.log('im here');
		let ims=document.getElementsByClassName('imx');
		let bts=document.getElementsByClassName('rtbb');
		for(var i=0;i<ims.length;i++)
		{
			if(elem==bts[i])
				{

					if(bts[i].dataset.imval==0)
						bts[i].dataset.imval=ims[i].width;
					let val=elem.value;
					ims[i].width=(val/100)*bts[i].dataset.imval;
				}
		}
	}
function assignEventListenerImageForm()
	{
		let elem=document.querySelector('#imageForm1');
		elem.addEventListener('submit',
			                  (event)=>
			                      {
			                      	// event.preventDefault();
			                      	takeComponentCount();
			                      	console.log("i was called");
			                      	let fileval=document.querySelector('#filein1').value;
			                      	if(fileval=='')
			                      	{
			                      		showModal_k("Error","You have to select a file first");
			                      		event.preventDefault();
			                      	}
			                      	// elem.submit();//kmhere this might be dangerous 
			                      }
			                 );
	}
function updateReview(productId,review)
	{
		let url='/submit-review/';
		fetch(url,
				  {
				  	method:'POST',
				  	headers:{
				  			  "Content-Type":"application/json",
				  			  "X-CSRFToken" :retrieveCookie('csrftoken'),
				  	 		},
				  	body   : JSON.stringify(
				  							 {
				  							 	"productId":productId,
				  							 	"rev"      :review,
				  							 }
				  						   )
				  }
			 )
		.then(
				response=>response.json()
			 )
		.then(
				data=>{
						//console.log("data:"+data);
			  		  	if(data.msg=='error')
			  		  		showModal_k("error",data.msg2);			  		  	
			  		  	else
			  		  	location.reload();
					  }
			 )
		.catch(
			    err=>
			    	 {
			    	 	showModal_k("Frontend error",err);
			    	 } 
			  );
			 
			 
		return true;
	}
function updateRating(rating,productId)
	{ //todo
		var url='/update_rating/';
		fetch(url,
				  {
				  	method:'POST',
				  	headers:{
				  			  'Content-Type':'application/json',
				  			   "X-CSRFToken":retrieveCookie('csrftoken'),
				  			},
				  	body: JSON.stringify(
				  						  {
				  						  	"productId":productId,
				  						  	"rating"   :rating,
				  						  }
				  		                )
				  }
			 )
		.then(
			  response=>response.json()
			 )
		.then(
			  (data)=>
			  		  {
			  		  	//console.log("data:"+data);
			  		  	if(data.msg=='authenticationerror')
			  		  		showModal_k("error","You have to be logged in");
			  		  	else if (data.msg=="servererror")
			  		  		showModal_k("error","Fatal error at server side");
			  		  	else
			  		  	location.reload();
			  		  }
			 );
		
	}
function fixEventListToRatingBtns()
	{
		var btns=document.getElementsByClassName('update-rating');
		for(var i=0;i<btns.length;i++)
			{

				btns[i].addEventListener('click',
												  function()
												  	{
												  		let rating=this.dataset.val;
												  		let productId=this.dataset.pid;

												  		if(confirm(`You are about to rate this product at ${rating} stars`))
											   	  			{
											   	  			updateRating(rating,productId);
											   	  			}
												  	}
										 );
			}
	}

function fixEventListToReviewBtns()
	{
		var btns=document.getElementsByClassName('update-review');
		for(var i=0;i<btns.length;i++)
			{

				btns[i].addEventListener('click',
												  function()
												  	{
												  		let review=document.querySelector("#rrev").value;
												  		if(review.trim()=="")
											   	  			{
											   	  			showModal_k("Error","You cant post a blank review");
											   	  			return false;
											   	  			}
											   	  		else if(review.trim().length<3)
											   	  			{
											   	  			showModal_k("Error",`${review}? What is that supposed to mean? uh`);
											   	  			return false;
											   	  			}
												  		let productId=this.dataset.pid;
												  		updateReview(productId,review);												  		
												  	}
										 );
			}
	}
function reg_login_formchecker(event)
	{
		let username=document.querySelector("#username").value;
		let password=document.querySelector("#password").value;
		let hidval=document.querySelector("#hidval").value;
		if(username.trim()=='' || password.trim()=='')
			{
				// if(hidval=="1") alert(1);
				// else alert(0);
				showModal_k("Error","Username or Password cannot be left blank");
				event.preventDefault();
			}
	}
function assignEventListenerToRegLogin()
	{
		let elems=document.getElementsByClassName("reglogin");
		// console.log(elems.length);
		for(var i=0;i<elems.length;i++)
		{
			elems[i].addEventListener('submit',event=>{reg_login_formchecker(event);});
		}
	}



function displayStoredComps()
	{
		let x=retrieveCookie('storex');
		if(x)
		{
			showModal_k("info",x);
		}
		else
		{
			showModal_k('info','looks like the cookie was not stored');
		}
	}

function storeToCookie(elem,cookieName="storex")
	{
		document.cookie=cookieName+'='+JSON.stringify(elem)+";domain=;path=/";
	}

function retrieveCookie(name) 
   	{
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') 
    	{
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) 
        	{
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) 
            	{
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            	}
        	}
    	}
    	return cookieValue;
	}

function fixButtonFuncAddStoryForm()
	{
		var frms=document.getElementsByClassName('actionBtn');
		for(var i=0;i<frms.length;i++)
		{
			frms[i].addEventListener('click',
									   function()
									   {
									   	if(this.dataset.func=='textbox')
									   		{
									   			let s_title=document.querySelector('#storytitle').value;
									   			let s_genre=document.querySelector('#storyGenre').value;
									   			if(s_title=="" || s_genre=="--")
									   				{
									   					showModal_k("Info","You have to select both a title and a genre before you proceed!! ");
									   					return false;
									   				}
									   				
									   			let texElems=document.getElementsByClassName('tb');

									   			if(texElems.length!=0 && texElems[texElems.length-1].value.trim()=='')
									   				{
									   					console.log(texElems[texElems.length-1].innerHTML);
									   					showModal_k("Unneccesary!","The last text box has no contents");
									   					return false;
									   				}

									   			vals_in_texboxes=store_vals_temp('tb');									   				
									   			let elem="<textarea rows='5' cols='100' class='tb addedElem' data-typex='tb'></textarea>";
									   			elem+="<br/><button class='btn btn-danger tbb' onclick='delx(this)'>delete</button>";
									   			document.querySelector('#workspace').innerHTML+=elem;
									   			reinstate_vals('tb',vals_in_texboxes);

									   		}
									   	else if(this.dataset.func=='imageload')
									   		{
									   			let file_path=document.querySelector('#filein1').value;
									   			showModal_k('info',file_path);

									   		}
									   	else if(this.dataset.func=='startx')
									   		{
									   			let s_title=document.querySelector('#storytitle').value;
									   			let s_genre=document.querySelector('#storyGenre').value;
									   			if(s_title=="" || s_genre=="--")
									   				{
									   					showModal_k("Info","You have to select both a title and a genre before you proceed!! ");
									   					return false;
									   				}
									   			document.querySelector('#toolButtons').style.display="";
									   			document.querySelector('#subBtn').style.display="";
									   		}
									   }
				              );
		}
	}

function submitStory()
	{
		let elems=document.getElementsByClassName('addedElem');
		let componentList=[];
		for (var i=0;i<elems.length;i++)
			{
				if(elems[i].dataset.typex=='tb')
				{
					componentList.push({"type":"textbox","content":elems[i].value});
				}
				else if(elems[i].dataset.typex=='im')
				{
					componentList.push({"type":"image","content":elems[i].src,"width":elems[i].width});
				}
			}
		sendToServer(componentList);
	}
function sendToServer(componentList)
	{
		let url='/submit-story/';
		let title=document.querySelector('#storytitle').value;
		let genre=document.querySelector('#storyGenre').value;
		let storyFinal='false';
		if(confirm("Your story is complete, correct? press cancel to say no"))
			storyFinal='true';
		if(title=="" || genre=="")
			{
				showModal_k("Cannot Proceed!!!","Either title or genre was found empty");
				return false;
			}

		fetch(url,
				  {
				  	method:'POST',
				  	headers:{
				  			  'Content-Type':'application/json',
				  			   "X-CSRFToken":retrieveCookie('csrftoken'),
				  			},
				  	body: JSON.stringify(
				  						  {
				  						  	"title":title,
				  						  	"genre":genre,
				  						  	"final":storyFinal,
				  						  	"comps":JSON.stringify(componentList),				  						  	
				  						  }
				  		                )
				  }
			 )
		.then(response=>response.json())
		.then(
				(data)=>
					    {
					    	console.log(data);
					    	// showModal_k("info",data.msg);
					    	window.location.href='/Home/';
					    }
			 )
		.catch(
				err=>{
					      showModal_k("Frontend error",err);
					 }
			  );
	}

function repaintBodyForLogin()
	{
		document.getElementsByTagName("body")[0].style.margin=0;
		document.getElementsByTagName("body")[0].style.padding=0;
		document.getElementsByTagName("body")[0].style.fontFamily="sans-serif";
		document.getElementsByTagName("body")[0].style.background="url('../static/media/bg.jpg') no-repeat";
		document.getElementsByTagName("body")[0].style.backgroundSize="cover";
	}