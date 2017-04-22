class ListStyle(object):
    @staticmethod
    def list(select, request):
        # select is a selection of resource like User.select()
        # request is a request object
        page_no = int(request.args.get('page', 1))
        results_per_page = int(request.args.get('number', 10))

        data_for_resp = ListStyle.get_data(select, page_no, results_per_page)
        urls_for_resp = ListStyle.get_next_prev_urls(
            request,
            page_no,
            results_per_page,
            len(data_for_resp)
        )

        return { 'data': data_for_resp, 'paging': urls_for_resp }

    @staticmethod
    def get_data(select, page_no, results_per_page):
        data = []
        end_ind = page_no*results_per_page
        start_ind = end_ind - results_per_page

        for record in select[start_ind:end_ind]:
            data.append(record.to_hash())

        return data

    @staticmethod
    def get_next_prev_urls(request, page_no, results_per_page, results_len):
        base_url = request.url.split('?')[0]
        if page_no > 1:
            prev_url = ("{base_url}?number={results_per_page}&page={prev_page_no}"
                        .format(
                            base_url=base_url,
                            results_per_page=results_per_page,
                            prev_page_no=page_no - 1
                        ))
        else:
            prev_url = None

        if results_len == results_per_page:
            next_url = ("{base_url}?number={results_per_page}&page={prev_page_no}"
                        .format(
                            base_url=base_url,
                            results_per_page=results_per_page,
                            prev_page_no=page_no + 1
                       ))
        else:
            next_url = None

        return { 'next': next_url, 'previous': prev_url }
