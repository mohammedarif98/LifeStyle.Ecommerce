// $(document).ready(function(){

//     $('.paywithrazorpay').click(function(e){
//         e.preventDefualt();

//         var name = $("[name='name']").val();
//         var number = $("[name='number']").val();
//         var email = $("[name='email']").val();
//         var pincode = $("[name='pincode']").val();
//         var state = $("[name='state']").val();
//         var city = $("[name='city']").val();
//         var address = $("[name='address']").val();

//         if(name=="" || number=="" || email=="" || pincode=="" || state=="" || city=="" || address=="")
//         {
//             alert('All Fields are Mandotory')
//             // swal("Alert !", "All Fields are Mandotory", "error");
//             return false
//         }
//         else
//         {

//             $.ajax({
//                 method : 'GET',
//                 url : '/proceed-to-pay',
//                 success : function(response){
//                     // console.log(response)
//                     var options = {
//                         "key": "rzp_test_01aNjwvOUNKwY4", // Enter the Key ID generated from the Dashboard
//                         "amount": response.pay_total_price, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
//                         "currency": "INR",
//                         "name": "LifeStyle",
//                         "description": "Thank You For Buy WithUs",
//                         "image": "https://example.com/your_logo",
//                         "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
//                         "handler": function (response){
//                             alert(response.razorpay_payment_id);
//                             alert(response.razorpay_order_id);
//                             alert(response.razorpay_signature)
//                         },
//                         "prefill": {
//                             "name": name,
//                             "email": email,
//                             "contact": number
//                         },
                        
//                         "theme": {
//                             "color": "#3399cc"
//                         }
//                     };
//                     var rzp1 = new Razorpay(options);
//                     rzp1.open();
//                 }
//             })

           
//         }

    
//     });

// })