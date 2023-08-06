## -*- coding: utf-8 -*-
<%inherit file="/reports/base.mako" />

<%def name="title()">Report : Inventory Worksheet</%def>

<%def name="page_content()">
  % if use_buefy:

      <p class="block">
        Please provide the following criteria to generate your report:
      </p>

      ${h.form(request.current_route_url())}
      ${h.csrf_token(request)}

      <b-field label="Department">
        <b-select name="department">
          <option v-for="dept in departments"
                  :key="dept.uuid"
                  :value="dept.uuid">
            {{ dept.name }}
          </option>
        </b-select>
      </b-field>

      <b-field>
        <b-checkbox name="weighted-only">
          Only include items which are sold by weight.
        </b-checkbox>
      </b-field>

      <b-field>
        <b-checkbox name="exclude-not-for-sale" :value="true">
          Exclude items marked "not for sale".
        </b-checkbox>
      </b-field>

      <div class="buttons">
        <b-button type="is-primary"
                  native-type="submit"
                  icon-pack="fas"
                  icon-left="arrow-circle-right">
          Generate Report
        </b-button>
      </div>

      ${h.end_form()}

  % else:

      <p>Please provide the following criteria to generate your report:</p>
      <br />

      ${h.form(request.current_route_url())}
      ${h.csrf_token(request)}

      <div class="field-wrapper">
        <label for="department">Department</label>
        <div class="field">
          <select name="department">
            % for department in departments:
                <option value="${department.uuid}">${department.name}</option>
            % endfor
          </select>
        </div>
      </div>

      <div class="field-wrapper">
        ${h.checkbox('weighted-only', label="Only include items which are sold by weight.")}
      </div>

      <div class="field-wrapper">
        ${h.checkbox('exclude-not-for-sale', label="Exclude items marked \"not for sale\".", checked=True)}
      </div>

      <div class="buttons">
        ${h.submit('submit', "Generate Report")}
      </div>

      ${h.end_form()}

  % endif
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ThisPageData.departments = ${json.dumps([{'uuid': d.uuid, 'name': d.name} for d in departments])|n}

  </script>
</%def>


${parent.body()}
