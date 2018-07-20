# Open Source Python POS and Accounting Software
<h3>Vision</h3>
<br />
<p>
  Pakistan has small to medium scale business running on manual paper-based records. After investigation, I have identified that the reluctance is channeled by the following reasons:
  <ol>
    <li>Complacency</li>
    <li>Fear of the unknown (software)</li>
    <li>Expensive Hardware</li>
    <li><b>Expensive Software</b></li>
    <li><b>Cost of updates</b></li>
  </ol>
  Software vendors can charge unreasonable rates from their clients for updates to the software as long as these (unreasonable) rates are less than the cost of new software from another vendor. This practice borders on bullying and is fairly common place.
  <br /> <br />
  Sometimes updates are not even possible because the vendor has closed shop and their propritary code is not available.
  <br /> <br />
  I have tried to tackle the last two issues, since they are within the scope of software. Something I meddle in.
  <br /> <br />
  I have built an open source software which suits the needs of a small to medium scale business. It is completely free to build and deploy.
  <br /> <br />
  My vision is to see the following changes in society and the business landscape:
  <ol>
    <li>More businesses keeping digital records</li>
    <li>Businesses not afraid of being bullied by software vendors for updates</li>
    <li>Employment opportunity of deploying the software</li>
    <li>Employment opportunity of improving and selling this software</li>
    <li>Employment opportunity of Data Analytics and Business Intelligence</li>
   </ol>
</p>
<br />
<h3>Description</h3>
<br />
<ol>
	<li><a href="https://github.com/HH95/Open-Source-Python-POS-and-Accounting-Software/wiki">Screenshots</a></li>
	<li>This software is written using Python 3 and wxPython (Pheonix).</li>
	<li>It has so far been tested on Linux.</li>
</ol>

<h3>Features</h3>
<br />
<h4>Point of Sale</h4>
<br />
<ol>
	<li>Functionality to query and add products by Barcode Number, Name and Code Name.</li>
	<li>Associate customer with each sale and purchase using their unique contact mobile phone number.</li>
	<li>Apply discount of individual products and the entire sale.</li>
	<li>Sale with cash (full payment), cheque (credit sale), purchase and return both sales and purchase.</li>
	<li>Update cash collected/paid against credit sales/purchase with cheque numbers.</li>
</ol>
<br />
<h4>Accounting</h4>
<br />
<ol>
	<li>Make <b>automated General Journal Entries</b> with each sale, purchase and returns of both. These entries are made in <u>Sale, Purchase, Cash, Accounts Recievable and Accounts Payable of Individual Customers.</u></li>
	<li>Make manual General Journal Entries</li>
	<li>Edit existing entries</li>
	<li>Display accounts of each Head of Account</li>
	<li>Maintain Accounts Recievable and Payable of each customer</li>
	<li>Create Control Account</li>
	<li>Create Income Statement</li>
	<li>All accounts mentioned above can be viewed for any date range</li>
</ol>
<br />
<h4>ERP</h4>
<br />
<ol>
	<li>Access rights and permissions of fellow users can be controlled through their login accounts</li>
</ol>
<br />
<h4>Future Plans</h4>
<br />
<ol>
	<li>Add Depreciation and Inventory Valuation</li>
	<li>Include BI Dashboard</li>
	<li>Make Windows Executable</li>
</ol>
<br />
<h3>Development and Technicalities</h3>
<br />
I have built this software using Python3. It uses <a href="https://github.com/PyMySQL/PyMySQL">PyMySQL</a> and <a href="https://wxpython.org/Phoenix/docs/html/index.html">WxPython</a>.
<br />
To understand the design start following the code starting from <a href="https://github.com/HH95/Open-Source-Python-POS-and-Accounting-Software/blob/master/mainInterface.py">mainInterface.py</a>.
