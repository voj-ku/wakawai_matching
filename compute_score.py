class Matcher:
    """
    A class to represent a matcher for non-profits and companies.
    """

    importances = {
        'category': 1,
        'sub-category': 1,
        'field-of-influence': 0.8,
        'collab-intensity': 0.2,
        'employee-involvement': 0.6,
        'form-of-help': 0.8,
        'expertises': 0.6,
        'barriers': 0.6,
        'reason-for-impact': 0.4,
    }

    category_scores = {
        0: 0,  # no overlap -> 0
        1: 0.75,  # single category -> 75%
        2: 1  # two overlaps -> 100%
    }

    subcategory_scores = {
        0: 0.4,
        1: 0.8,
        2: 0.8,
        3: 0.85,
        4: 0.85,
        5: 0.9,
        6: 0.9,
        7: 0.95,
        8: 0.95,
        9: 1,
        10: 1
    }

    form_of_help_scores = {
        0: 0.2,
        1: 0.8,
        2: 0.85,
        3: 0.9,
        4: 0.95,
        5: 1}

    expertises_scores = {
        0: 0.2,
        1: 0.5,
        2: 0.7,
        3: 0.8,
        4: 0.9,
        5: 1}

    barrier_scores = {
        0: 1,
        1: 0.8,
        2: 0.6,
        3: 0.2}

    reasons_for_impact_scores = {
        0: 0.4,
        1: 0.6,
        2: 0.7,
        3: 0.8,
        4: 0.9,
        5: 1}

    def __init__(self):
        self.nimps = {
            k: v / sum(self.importances.values()) for k, v in self.importances.items()}
        print('self.nimps', self.nimps)
        pass

    def _compute_overlap_score(self, org_data: list, firm_data: list, score_dict: dict) -> float:
        """
        Computes a score based on the number of common items between two lists, using a provided score dictionary.

        Args:
            org_data (list): A list of data from the organization.
            firm_data (list): A list of data from the firm.
            score_dict (dict): A dictionary mapping the number of overlapping items to a score.

        Returns:
            float: The computed score.
        """

        intersection = len(set(org_data) & set(firm_data))
        # Get score, default to 0 if not found
        score = score_dict.get(intersection, 0)
        return score

    # 1 - category
    def category_score(self, org: dict, firm: dict) -> float:
        """
        Computes a score based on the number of common category between an organization and a firm.

        Args:
            org (dict): A dictionary representing the organization, with a "category" key containing a list of category.
            firm (dict): A dictionary representing the firm, with a "category" key containing a list of category.

        Returns:
            float: The computed score.
        """
        try:
            return self._compute_overlap_score(org['category'], firm['category'], self.category_scores)
        except KeyError as e:
            print(f"Missing key: {e}")
            return 0  # Or handle the error as you see fit

    # 2 - sub-category
    def subcategory_score(self, org: dict, firm: dict) -> float:
        """
        Computes a score based on the number of common sub-category between an organization and a firm.

        Args:
            org (dict): A dictionary representing the organization, with a "sub-category" key containing a list of sub-category.
            firm (dict): A dictionary representing the firm, with a "sub-category" key containing a list of sub-category.

        Returns:
            float: The computed score.
        """
        try:
            return self._compute_overlap_score(org['sub-category'], firm['sub-category'], self.subcategory_scores)
        except KeyError as e:
            print(f"Missing key: {e}")
            return 0  # Or handle the error as you see fit

    # 3 - field of influence
    def field_of_influence_score(self, org: dict, firm: dict) -> float:
        """
        Computes a score based on the fields of influence between an organization and a firm.

        Args:
            org (dict): A dictionary representing the organization, with a "field-of-influence" key containing a value for the fields of influence.
            firm (dict): A dictionary representing the firm, with a "field-of-influence" key containing a value for the fields of influence.

        Returns:
            float: The computed score.
        """
        try:
            if firm['field-of-influence'] == org['field-of-influence']:
                return 1

            elif sorted([firm['field-of-influence'], org['field-of-influence']]) in [
                ['czechia', 'global'],
                ['czechia', 'regional'],
                ['global', 'regional']
            ]:
                return 0.3

            else:
                return 0
        except KeyError as e:
            print(f"Missing key: {e}")
            return 0  # Or handle the error as you see fit

    # 4 - collaboration intensity
    def collaboration_intensity_score(self, org: dict, firm: dict) -> float:
        """
        Computes a score based on the preferred collaboration intensity between an organization and a firm.

        Args:
            org (dict): A dictionary representing the organization, with a "collaboration-intensity" key containing a value for the fields of influence.
            firm (dict): A dictionary representing the firm, with a "collaboration-intensity" key containing a value for the fields of influence.

        Returns:
            float: The computed score.
        """
        try:
            # assume it's either one-time or multiple
            if org['collab-intensity'] == firm['collab-intensity']:
                return 1
            else:
                return 0.5
        except KeyError as e:
            print(f"Missing key: {e}")
            return 0  # Or handle the error as you see fit

    # 5 - employee involvement
    def employee_involvement_score(self, org: dict, firm: dict) -> float:
        """
        Computes a score based on the preferred employee involvement of an organization and a firm.

        Args:
            org (dict): A dictionary representing the organization, with an "employee-involvement" key containing a value for employee involvement preference ('yes' or 'no').
            firm (dict): A dictionary representing the firm, with an "employee-involvement" key containing a value for employee involvement preference ('yes' or 'no').

        Returns:
            float: The computed score. 1 if both prefer involvement, 0.8 if only the organization prefers it, 0.3 if only the firm prefers it.
        """
        try:
            if org['employee-involvement'] == firm['employee-involvement']:
                return 1
            elif org['employee-involvement'] != 'yes' and firm['employee-involvement'] == 'no':
                return 0.8
            elif org['employee-involvement'] == 'no' and firm['employee-involvement'] == 'yes':
                return 0.3
            else:
                return 0

        except KeyError as e:
            print(f"Missing key: {e}")
            return 0  # Or handle the error as you see fit

    # 6 - form of help
    def form_of_help_score(self, org: dict, firm: dict) -> float:
        try:
            return self._compute_overlap_score(org_data=org['form-of-help'], firm_data=firm['form-of-help'], score_dict=self.form_of_help_scores)
        except KeyError as e:
            print(f"Missing key: {e}")
            return 0  # Or handle the error as you see fit

    # 7 - expertises
    def expertise_score(self, org: dict, firm: dict) -> float:
        try:
            return self._compute_overlap_score(org_data=org['expertises'], firm_data=firm['expertises'], score_dict=self.expertises_scores)
        except KeyError as e:
            print(f"Missing key: {e}")
            return 0  # Or handle the error as you see fit

    # 8 - barriers to help
    def barriers_score(self, org: dict, firm: dict) -> float:
        try:
            return self._compute_overlap_score(org_data=org['barriers'], firm_data=firm['barriers'], score_dict=self.barrier_scores)
        except KeyError as e:
            print(f"Missing key: {e}")
            return 0  # Or handle the error as you see fit

    # 9 - why have positive impact
    def impact_reasons_score(self, org: dict, firm: dict) -> float:
        try:
            return self._compute_overlap_score(org_data=org['reason-for-impact'], firm_data=firm['reason-for-impact'], score_dict=self.reasons_for_impact_scores)
        except KeyError as e:
            print(f"Missing key: {e}")
            return 0  # Or handle the error as you see fit

    def compute_match_score(self, org: dict, firm: dict) -> float:
        """
        Computes the overall match score between an organization and a firm.

        Args:
            org (dict): A dictionary representing the organization.
            firm (dict): A dictionary representing the firm.

        Returns:
            float: The overall match score.
        """

        self.unweighed_scores = {
            'category': self.category_score(org, firm),
            'sub-category': self.subcategory_score(org, firm),
            'field-of-influence': self.field_of_influence_score(org, firm),
            'collab-intensity': self.collaboration_intensity_score(org, firm),
            'employee-involvement': self.employee_involvement_score(org, firm),
            'form-of-help': self.form_of_help_score(org, firm),
            'expertises': self.expertise_score(org, firm),
            'barriers': self.barriers_score(org, firm),
            'reason-for-impact': self.impact_reasons_score(org, firm),
        }

        print('self.unweighed_scores', self.unweighed_scores)

        self.weighed_scores = {
            'category': self.unweighed_scores['category'] * self.nimps['category'],
            'sub-category': self.unweighed_scores['sub-category'] * self.nimps['sub-category'],
            'field-of-influence': self.unweighed_scores['field-of-influence'] * self.nimps['field-of-influence'],
            'collab-intensity': self.unweighed_scores['collab-intensity'] * self.nimps['collab-intensity'],
            'employee-involvement': self.unweighed_scores['employee-involvement'] * self.nimps['employee-involvement'],
            'form-of-help': self.unweighed_scores['form-of-help'] * self.nimps['form-of-help'],
            'expertises': self.unweighed_scores['expertises'] * self.nimps['expertises'],
            'barriers': self.unweighed_scores['barriers'] * self.nimps['barriers'],
            'reason-for-impact': self.unweighed_scores['reason-for-impact'] * self.nimps['reason-for-impact'],
        }
        print(self.weighed_scores)
        overall_score = sum(self.weighed_scores.values())

        return overall_score
